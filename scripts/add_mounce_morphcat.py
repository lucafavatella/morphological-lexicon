#!/usr/bin/env python

from collections import defaultdict
import sys
import unicodedata

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml

def n(x):
    return unicodedata.normalize("NFKC", x)

lexemes = load_yaml("lexemes.yaml")

mounce = defaultdict(list)
with open("../data-cleanup/mounce-morphcat/mounce-tauber-morphcat-utf8.txt") as f:
    for line in f:
        gk, greek, morphcat = line.strip().decode("utf-8").split(":")
        greek = n(greek)
        mounce[greek].append({
            "gk": gk,
            "morphcat": morphcat,
        })

problems = []
for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    print "{}:".format(lexeme.encode("utf-8"))
    print "    pos: {}".format(metadata["pos"])
    
    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
    
    q("bdag-headword")
    q("dodson-entry")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    
    if "mounce-morphcat" in metadata:
        print "    {}: {}".format("mounce-morphcat", metadata["mounce-morphcat"])
    else:
        if lexeme in mounce:
            source = lexeme
        elif metadata.get("bdag-headword") in mounce:
            source = metadata["bdag-headword"]
        else:
            source = None
        if source:
            if len(mounce[source]) == 1:
                try:
                    gk = int(mounce[source][0]["gk"])
                except ValueError:
                    gk = None
                if metadata.get("gk") == gk:
                    print "    mounce-morphcat: {}".format(mounce[source][0]["morphcat"])
                else:
                    problems.append("{} {} != {}".format(source.encode("utf-8"), metadata.get("gk"), gk))
            else:
                problems.append("{} len({}) > 1".format(source.encode("utf-8"), mounce[source]))
        else:
            problems.append("{} not found (gk={})".format(lexeme.encode("utf-8"), metadata["gk"]))


print >>sys.stderr, "problems"
for problem in problems:
    print >>sys.stderr, "\t", problem
print >>sys.stderr, "{}".format(len(problems))
