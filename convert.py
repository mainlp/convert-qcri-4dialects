"""
Converts annotated corpus files with the format:
TOKEN	TAG
(tab-separated).
Sentence boundaries are indicated by empty lines.
"""

from argparse import ArgumentParser


def ara(in_file, out_file, include_tag_details=True, print_mapping=False,
        print_segment_details=True):
    replace3 = {
        "DET+ADJ+CASE": "ADJ+__+__",
        "DET+ADJ+NSUFF": "ADJ+__+__",
        "DET+NOUN+CASE": "NOUN+__+__",
        "DET+NOUN+NSUFF": "NOUN+__+__",
    }
    replace2 = {
        "+CASE": "+__",
        "+NSUFF": "+__",
        "DET+ADJ": "ADJ+__",
        "DET+NOUN": "NOUN+__",
        "PROG_PART+V": "V+__",
    }
    replace1 = {
        "CONJ": "CCONJ",
        "EMOT": "SYM",
        "FOREIGN": "X",
        "FUT_PART": "AUX",
        "HASH": "X",
        "MENTION": "PROPN",
        "NEG_PART": "PART",
        "PREP": "ADP",
        "PUNC": "PUNCT",
        "URL": "SYM",
        "V": "VERB",
    }
    replace_last = {
        "ADVERB": "ADV",  # introduced by V->VERB change
    }
    replacement_dicts = (replace3, replace2, replace1, replace_last)
    replace_fulltok = {
        # On their own:
        # https://universaldependencies.org/u/dep/all.html#al-u-dep/goeswith
        "CASE": "X",
        "NSUFF": "X",
        "PROG_PART": "X",
        # Annotation mistake?
        "PROG_PART+NOUN": "X+NOUN",
        # Segmentation mistake?
        "PART+PROG_PART": "PART+X",
    }

    part2sconj_forms = ["إن", "ان", "أن"]  # PADT SCONJ forms
    part2sconj_forms += ["إِن", "إِنَّ", "أَن", "أَنَّ"]  # PADT SCONJ lemmas
    tag_map = {}
    n_not_split = 0
    n_segments_ok = 0
    segment_issues = []
    with open(out_file, 'w+', encoding="utf8") as f_out:
        with open(in_file, encoding="utf8") as f_in:
            first_line = True
            sent = ""
            skip_sent = False
            for line in f_in:
                line = line.strip()
                if not line:
                    continue
                if first_line:
                    first_line = False
                    continue
                cells = line.split("\t")
                form = cells[4]
                pos = cells[6]
                if pos == "EOS":
                    if not skip_sent:
                        f_out.write(sent + "\n")
                    sent = ""
                    skip_sent = False
                    continue
                if skip_sent:
                    continue
                if not form:
                    print("Line with empty token (skipping sentence):")
                    print(line)
                    skip_sent = True
                    continue
                for repl_dict in replacement_dicts:
                    for repl in repl_dict:
                        if repl in pos:
                            pos = pos.replace(repl, repl_dict[repl])
                for re_full in replace_fulltok:
                    if re_full == pos:
                        pos = replace_fulltok[re_full]
                tag_map[cells[6]] = pos
                use_segments = False
                tags = pos.split("+")
                if len(tags) > 1:
                    for tag in tags[1:]:
                        if tag != "__":
                            use_segments = True
                            break
                    if not use_segments:
                        sent += f"{form}\t{tags[0]}"
                        if include_tag_details:
                            sent += f"\t{cells[6]}\t{0}:{len(tags)}\n"
                        else:
                            sent += "\n"
                        n_not_split += 1
                        continue
                if use_segments:
                    segments = cells[5].split("+")
                    n = len(tags)
                    assert n == len(segments)
                    i = 0
                    while i < n:
                        j = i + 1
                        while j < n:
                            if tags[j] == "__":
                                j += 1
                            else:
                                break
                        joined_form = "".join(segments[i:j])
                        all_joined = "".join(segments)
                        if all_joined == form:
                            n_segments_ok += 1
                        else:
                            segment_issues.append(
                                (form, all_joined, cells[5]))
                        joined_tag = tags[i]
                        sent += f"{joined_form}\t{joined_tag}"
                        if include_tag_details:
                            sent += f"\t{cells[6]}\n"
                        else:
                            sent += "\n"
                        i = j
                    continue
                if pos == "PART" and form in part2sconj_forms:
                    pos = "SCONJ"
                sent += f"{form}\t{pos}\n"
                n_not_split += 1
    if print_mapping:
        print("Mapped the original tags as follows:")
        for orig_tag in tag_map:
            print(f"{orig_tag}\t{tag_map[orig_tag]}")
    if print_segment_details:
        print("Full token used:", n_not_split)
        print("Segmentation used -- segmentation OK:", n_segments_ok)
        print("Segmentation used -- issues with segmentation:",
              len(segment_issues))
        for issue in segment_issues:
            print(f"tok {issue[0]} merged {issue[1]} segments {issue[2]}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dir", default="",
                        help="data directory root")
    parser.add_argument("--files", default="",
                        help="input file(s) within the data directory, "
                        "comma-separated")
    parser.add_argument("--out", help="output file")
    parser.add_argument("--include_tag_details", default=False,
                        action="store_true")
    args = parser.parse_args()
    ara(args.dir + "/" + args.files, args.out, args.include_tag_details)
