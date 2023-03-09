# qcri_dialectal-arabic-resources_UPOS

This script converts the [Four Arabic Dialects POS tagged Dataset](https://github.com/qcri/dialectal_arabic_resources) ([released under the Apache License 2.0](https://alt.qcri.org/resources/da_resources/); article: [Darwish ea 2018](https://aclanthology.org/L18-1015/)) to [UPOS](https://universaldependencies.org/u/pos/) tags.

It was used for the paper *TBD*.

## Usage

```
# Optional preliminary check:
python3 check_arabic_segmentation.py dialectal_arabic_resources/seg_plus_pos_egy.txt dialectal_arabic_resources/seg_plus_pos_lev.txt dialectal_arabic_resources/seg_plus_pos_glf.txt dialectal_arabic_resources/seg_plus_pos_mgr.txt  > arabic_preprocessing.log

# The actual data conversion:
python3 corpus_prep.py --dir dialectal_arabic_resources/ --files seg_plus_pos_egy.txt --out dev_dar-egy_UPOS.tsv
python3 corpus_prep.py --dir dialectal_arabic_resources/ --files seg_plus_pos_glf.txt --out test_dar-glf_UPOS.tsv
python3 corpus_prep.py --dir dialectal_arabic_resources/ --files seg_plus_pos_lev.txt --out test_dar-lev_UPOS.tsv
python3 corpus_prep.py --dir dialectal_arabic_resources/ --files seg_plus_pos_mgr.txt --out test_dar-mgr_UPOS.tsv

# Optional checks:
python3 validate_converted_file.py dev_dar-egy_UPOS.tsv tagset_upos.txt
python3 validate_converted_file.py test_dar-glf_UPOS.tsv tagset_upos.txt
python3 validate_converted_file.py test_dar-lev_UPOS.tsv tagset_upos.txt
python3 validate_converted_file.py test_dar-mgr_UPOS.tsv tagset_upos.txt
```

## Details

(See also Appendix B of our paper *TBD*. The inverse table (sorted by UPOS tag) can also be found there.)

Relevant documentation:
- "[Multi-Arabic POS tagging: A CRF approach](https://aclanthology.org/L18-1015/)" (Darwish ea, LREC 2018) -- the paper describing the corpus
- "[Using stem-templates to improve Arabic POS and gender/number tagging](https://aclanthology.org/L14-1296/)"" (Darwish ea, LREC 2014) -- information on the *Farasa* tagset on which the corpus's tagset is based
- the corpus description pages for [Arabic treebanks](https://universaldependencies.org/ar/index.html) in general and for *UD Arabic PADT*](https://universaldependencies.org/treebanks/ar_padt/) in particular
- "[Treebanking user-generated content: a UD based overview of guidelines, corpora and unified recommendations](https://link.springer.com/article/10.1007/s10579-022-09581-9)" (Sanguinetti ea, LRE 2022)
- [Arabic Dialects Segmentation Guidelines](https://alt.qcri.org/wp-content/uploads/2020/08/seg-guidelines.pdf) -- the guidelines according to which the corpus was originally segmented
- "A reference grammar of Modern Standard Arabic" (Ryding 2005, Cambridge University Press)
- "The syntax of spoken Arabic" (Brustad 2000, Georgetown University Press)

| Original tag | Description | UPOS| Note |
| ----- | ----- | ----- | ----- |
| ABBREV | Abbreviation |  | not in dataset |
| ADJ | Adjective | ADJ | restore merged sequences where relevant: (DET+)ADJ(+CASE/NSUFF) -> ADJ |
| ADV | Adverb | ADV| -- |
| CASE | Case (tanween)  | merged with NOUN/ADJ morphemes where possible, otherwise X |  |
| CONJ | Conjunction | CCONJ, (SCONJ) | [UD Arabic documentation](https://universaldependencies.org/ar/index.html#tags): "subordinating and coordinating conjunctions are not distinguished (the CCONJ tag is used)", although there is an [exception for a small group of subordinating conjunctions/particles](https://universaldependencies.org/treebanks/ar_padt/ar_padt-pos-SCONJ.html) (cf. Ryding pp. 422, 611, 673) |
| DET | Determiner | DET | merged with NOUN/ADJ morphemes where possible |
| EMOT | Emoji | SYM | -- |
| FOREIGN | Foreign words, non-words | X | |
| FUT_PART | Prefix or particle marking future tense | AUX | |
| HASH | Hashtag | X | Using the actual POS tag as recommended by Sanguinetti ea is too difficult. Settling for X since it 1. matches what several other treebanks are doing, and 2. matches that non-Arabic tokens are X, and many hashtags are non-Arabic too (although there also are many Arabic hashtags). |
| JUS | Jussive form of verb | | not in dataset, but would be VERB with Mood=Jus |
| MENTION | Mention | PROPN | per Sanguinetti ea's recommendation |
| NEG_PART | Negation particle | PART | |
| NOUN | Noun | NOUN | restore merged sequences where relevant: (DET+)NOUN(+CASE/NSUFF) -> NOUN |
| NSUFF | Noun suffix | merged with NOUN/ADJ morphemes where possible, otherwise X |  |
| NUM | Number | NUM| -- |
| PART | Particle | PART, SCONJ | see below |
| PREP | Preposition | ADP | -- |
| PROG_PART | Progressive particle | merged with VERB morphemes where possible, otherwise X | can be marked with Aspect=Prog when joined with a verb; a potentially tricky assignment as progressivity is handled differently in MSA and non-standard Arabic (Brustad pp. 142, 246/7) |
| PRON | Pronoun | PRON | -- |
| PUNC | Punctuation | PUNCT | -- |
| URL | URL | SYM | |
| V | Verb | VERB | -- |
| VSUFF | Verbal suffix |  | not in dataset |

