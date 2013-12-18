#!/usr/bin/env python

import sys

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml, load_wordset

lexemes = load_yaml("lexemes.yaml")
danker = load_yaml("../data-cleanup/danker-concise-lexicon/danker_headwords.yaml")
missing_danker = load_wordset("missing_danker.txt")

problems = []
skipped = 0

for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    print "{}:".format(lexeme.encode("utf-8"))
    print "    pos: {}".format(metadata["pos"])
    
    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
    
    q("bdag-headword")

    if "danker-entry" in metadata:
        print "    {}: {}".format("danker-entry", metadata["danker-entry"].encode("utf-8"))
    else:
        if lexeme in missing_danker:
            skipped += 1
            continue
                
        if lexeme in danker:
            entry = danker[lexeme]
        elif metadata.get("bdag-headword") in danker:
            entry = danker[metadata["bdag-headword"]]
        else:
            entry = None

        if entry:
            print "    {}: {}".format("danker-entry", entry.encode("utf-8"))
        else:
            problems.append("{} not found (bdag={})".format(lexeme.encode("utf-8"), metadata.get("bdag-headword", u"none").encode("utf-8")))


    q("dodson-entry")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")


print >>sys.stderr, "problems"
for problem in problems:
    print >>sys.stderr, "\t", problem
print >>sys.stderr, "{} ({} skipped)".format(len(problems), skipped)
