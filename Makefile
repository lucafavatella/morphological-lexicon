.PHONY: all
all: ;

.PHONY: add_dodson
add_dodson: \
		data-cleanup/dodson-lexicon/dodson_lexicon.txt \
		lexemes.yaml \
		missing_dodson.txt \
		twice_dodson.txt
	scripts/$@.py \
		- \
		$(word 2,$^) \
		--missing $(word 3,$^) \
		--twice $(word 4,$^) \
		--override dodson-entry \
		< $<

data-cleanup/dodson-lexicon/dodson_lexicon.txt: data-cleanup/dodson-lexicon/dodson.csv | scripts/beta_to_unicode.py
	scripts/clean_dodson.py < $< > $@

data-cleanup/dodson-lexicon/dodson.csv:
	curl -f -sS -o $@ --create-dirs https://raw.githubusercontent.com/biblicalhumanities/Dodson-Greek-Lexicon/5f140b84bd7541cd883acf9b1e0e43e383d677e6/dodson.csv

scripts/beta_to_unicode.py:
	{ echo '# -*- coding: utf-8 -*-' && curl -f -sS https://raw.githubusercontent.com/cltk/cltk/v0.1.46/cltk/corpus/greek/beta_to_unicode.py; } > $@
