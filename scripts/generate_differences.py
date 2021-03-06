#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import re
import sys
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", unicode(s)) if unicodedata.category(c) != "Mn"))


METADATA_NAMES = [
    "bdag-headword",
    "danker-entry",
    "dodson-entry",
    "mounce-headword",
]

fully_match = 0
no_tag = 0

for lexeme, metadata in sorted_items(lexemes):

    def r(metadata_name):
        v = metadata.get(metadata_name, "<missing>")
        if v:
            v = v.split(",")[0]
        return v if v != lexeme else None

    differences = defaultdict(list)
    for metadata_name in METADATA_NAMES:
        if r(metadata_name):
            differences[r(metadata_name)].append(metadata_name)

    if differences:
        print "{}:".format(lexeme.encode("utf-8"))
        for value, metadata_names in differences.items():
            tags = []
            if value.lower() == lexeme.lower():
                tags.append("case")
            elif strip_accents(value) == strip_accents(lexeme):
                tags.append("accentuation")
            elif strip_accents(value.lower()) == strip_accents(lexeme.lower()):
                tags.append("case")
                tags.append("accentuation")
            elif value.replace(u"οε", u"ου") == lexeme:
                tags.append("οε contraction")
            elif value.replace(u"εο", u"ου") == lexeme:
                tags.append("εο contraction")
            elif value.replace(u"όο", u"οῦ") == lexeme:
                tags.append("οο contraction")
            elif re.sub(u"ω$", u"ομαι", value) == lexeme:
                tags.append("ω/ομαι")
            elif re.sub(u"ω$", u"ομαι", strip_accents(value)) == strip_accents(lexeme):
                tags.append("ω/ομαι")
                tags.append("accentuation")
            elif re.sub(u"ομαι$", u"ω", value) == lexeme:
                tags.append("ω/ομαι")
            elif re.sub(u"ομαι$", u"ω", strip_accents(value)) == strip_accents(lexeme):
                tags.append("ω/ομαι")
                tags.append("accentuation")
            elif re.sub(u"η", u"ομαι", value) == lexeme:
                tags.append("η/ομαι")
            elif re.sub(u"ημι$", u"εμαι", value) == lexeme:
                tags.append("ημι/εμαι")
            elif re.sub(u"εμαι$", u"ημι", value) == lexeme:
                tags.append("ημι/εμαι")
            elif re.sub(u"ημι$", u"αμαι", value) == lexeme:
                tags.append("ημι/αμαι")
            elif re.sub(u"αμαι$", u"ημι", value) == lexeme:
                tags.append("ημι/αμαι")
            elif re.sub(u"υμι$", u"υμαι", value) == lexeme:
                tags.append("υμι/υμαι")
            elif strip_accents(value).replace(u"αννυμι", u"αμαι") == strip_accents(lexeme):
                tags.append("αννυμι/αμαι")
            elif strip_accents(value).replace(u"ς", u"τερος") == strip_accents(lexeme):
                tags.append("-τερος")
            elif strip_accents(value).replace(u"ος", u"ωτερος") == strip_accents(lexeme):
                tags.append("-τερος")
            elif strip_accents(value).replace(u"ς", u"τερον") == strip_accents(lexeme):
                tags.append("-τερον")
            elif strip_accents(value).replace(u"ως", u"εστερον") == strip_accents(lexeme):
                tags.append("-τερον")
            elif value.replace(u"ἐνδέχομαι", u"ἐνδέχεται") == lexeme:
                tags.append("ομαι/εται")
            elif re.sub(u"ον$", u"ος", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ος$", u"ον", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ός$", u"όν", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ον$", u"α", value) == lexeme:
                tags.append("ον/α")
            elif re.sub(u"α$", u"ον", value) == lexeme:
                tags.append("ον/α")
            elif re.sub(u"α$", u"ον", strip_accents(value)) == strip_accents(lexeme):
                tags.append("ον/α")
            elif re.sub(u"ος$", u"α", value) == lexeme:
                tags.append("ος/α")
            elif strip_accents(value).replace(u"ης", u"ος") == strip_accents(lexeme):
                tags.append("ης/ος")
            elif strip_accents(value).replace(u"ος", u"η") == strip_accents(lexeme):
                tags.append("η/ος")
            elif re.sub(u"όω$", u"άω", value) == lexeme:
                tags.append("οω/αω")
            elif strip_accents(re.sub(u"ύω$", u"ω", value)) == strip_accents(lexeme):
                tags.append("ύω/ω")
            elif re.sub(u"ω$", u"αω", strip_accents(value)) == strip_accents(lexeme):
                tags.append("ύω/ω")
            elif re.sub(u"α$", u"εν", value) == lexeme:
                tags.append("εν/α")
            elif re.sub(u"α$", u"η", value) == lexeme:
                tags.append("final η/α")
            elif value.replace(u"ληψ", u"λημψ") == lexeme:
                tags.append("(μ)π")
            elif value.replace(u"λήπ", u"λήμπ") == lexeme:
                tags.append("(μ)π")
            elif value.replace(u"ληπ", u"λημπ") == lexeme:
                tags.append("(μ)π")
            elif value.replace(u"(μ)π", u"μπ") == lexeme:
                tags.append("(μ)π")
            elif value.replace(u"πλ", u"μπλ") == lexeme:
                tags.append("(μ)π")
            elif value.replace(u"(ρ)ρ", u"ρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"ρρ", u"ρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"ρ", u"ρρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"δ(δ)", u"δ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"δδ", u"δ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"δ", u"δδ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"λ", u"λλ") == lexeme:
                tags.append("double λ")
            elif value.replace(u"νν", u"ν") == lexeme:
                tags.append("double ν")
            elif value.replace(u"σσ", u"σ") == lexeme:
                tags.append("double σ")
            elif value.replace(u"σ", u"σσ") == lexeme:
                tags.append("double σ")
            elif value.replace(u"γγ", u"γ") == lexeme:
                tags.append("double γ")
            elif value.replace(u"εί", u"ί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"ί", u"εί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"ει", u"ι") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"ει", u"ϊ") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ί", u"ί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ι", u"ι") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ί", u"εί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ι", u"ει") == lexeme:
                tags.append("ει/ι")
            elif strip_accents(value).replace(u"ει", u"ι") == strip_accents(lexeme):
                tags.append("ει/ι")
            elif value.replace(u"ει", u"η") == lexeme:
                tags.append("ει/η")
            elif value.replace(u"ε", u"αι") == lexeme:
                tags.append("αι/ε")
            elif value.replace(u"(ν)", u"") == lexeme:
                tags.append("movable ν")
            elif value.replace(u"(ν)", u"ν") == lexeme:
                tags.append("movable ν")
            elif value + u"(ν)" == lexeme:
                tags.append("movable ν")
            elif lexeme + u"ν" == value:
                tags.append("final ν")
            elif re.sub(u"ν$", u"(ν)", value) == lexeme:
                tags.append("movable ν")
            elif re.sub(u"ν$", u"μ", value) == lexeme:
                tags.append("final μ/ν")
            elif value + u"(ς)" == lexeme:
                tags.append("movable ς")
            elif re.sub(u"ς$", u"(ς)", value) == lexeme:
                tags.append("movable ς")
            elif re.sub(u"ς$", "", value) == lexeme:
                tags.append("movable ς")
            elif strip_accents(value) + u"ς" == strip_accents(lexeme):
                tags.append("movable ς")
                tags.append("accentuation")
            elif value.replace(u"τριοε", u"τριε") == lexeme:
                tags.append("τρι(ο)ε")
            elif value.replace(u"αττο", u"αττα") == lexeme:
                tags.append("αττο/αττα")
            elif value.replace(u"ιδάριον", u"αρίδιον") == lexeme:
                tags.append("ιδάριον/αρίδιον")
            elif value.replace(u"ερ", u"ηρ") == lexeme:
                tags.append("ε/η")
            elif value.replace(u"η", u"ι") == lexeme:
                tags.append("η/ι")
            elif value.replace(u"Ἀ", u"Ἁ") + u"χ" == lexeme:
                tags.append("final χ")
                tags.append("breathing")
            elif value.replace(u"ίας", u"ιᾶτος") == lexeme:
                tags.append("ίας/ιᾶτος")
            elif value.replace(u"όω", u"ίσκω") == lexeme:
                tags.append("όω/ίσκω")
            elif value.replace(u"εύ", u"αύ") == lexeme:
                tags.append("εύ/αύ")
            elif lexeme == u"Ἀππίου" and value == u"Ἄππιος":
                tags.append("inflected partial")
            elif "/" in value:
                tags.append("/ in value @@")
            elif " " in value:
                tags.append("space in value @@")
            else:
                if value != "<missing>":
                    tags.append("@@@")
                    no_tag += 1
            print "    {}:".format(value.encode("utf-8"))
            print "        {}: [{}]".format("tags", ", ".join("\"{}\"".format(tag) for tag in tags))
            print "        {}: [{}]".format("sources", ", ".join("\"{}\"".format(source) for source in metadata_names))
    else:
        fully_match += 1

print >>sys.stderr, "{} fully-match; {} no-tag".format(fully_match, no_tag)
