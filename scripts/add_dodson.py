#!/usr/bin/env python3

import argparse
from collections import defaultdict
import csv
import sys

import yaml

from morphgnt.utils import load_yaml, load_wordset, sorted_items
from morphgnt.utils import nfkc_normalize as n


def load_dodson(f):
    csv_in = csv.reader(f, dialect='excel-tab', strict=True)
    next(csv_in) # Skip field names row.

    dodson = defaultdict(list)
    for row in csv_in:
        [strongs, gk, greek, short_gloss, long_gloss] = row
        head_word = greek.split(",")[0].strip()
        gks = [int(v) for v in gk.split(",")]
        assert len(gks) > 0
        dodson[n(head_word)].append({
            "strongs": int(strongs),
            "gk": gks,
            "greek": n(greek),
            "short-gloss": short_gloss,
            "long-gloss": long_gloss
        })
    return dodson

def dump_lexemes(f, lexemes, dodson, overrides):
    missing_in_dodson = set()
    twice_in_dodson = set()
    for lexeme, metadata in sorted_items(lexemes):
        print("{}:".format(lexeme), file=f)

        data = dodson[lexeme] if lexeme in dodson \
               else dodson[metadata["bdag-headword"]] if ("bdag-headword" in metadata \
                                                          and metadata["bdag-headword"] in dodson) \
               else None
        if data is None:
            missing_in_dodson.add(lexeme)
        else:
            assert len(data) > 0, "{}: {}".format(lexeme, data)
            if len(data) == 1:
                data = data[0]
            else:
                twice_in_dodson.add(lexeme)
                data = None
        if data is not None:
            data["gk"] = yaml.dump(data["gk"]).strip() if isinstance(data["gk"], list) \
                         else data["gk"] ## TODO review.

        def l(metadata_name):
            """Keep metadata item from lexemes file if metadata item present there."""
            if metadata_name in metadata:
                print("    {}: {}".format(metadata_name, metadata[metadata_name]), file=f)

        def ld(metadata_name, data_name):
            """Keep metadata item from lexemes file if metadata item present there, otherwise from dodson if lexeme present there."""
            if metadata_name not in metadata and data is not None:
                print("    {}: {}".format(metadata_name, data[data_name]), file=f)
            else:
                l(metadata_name)

        l("pos")
        l("full-citation-form")
        l("bdag-headword")
        l("danker-entry")
        ld("dodson-entry", "greek")
        l("mounce-headword")
        ld("strongs", "strongs")
        ld("gk", "gk")
        l("dodson-pos")
        ld("gloss", "short-gloss")
        l("mounce-morphcat")

        ## TODO Use overrides.
        def p2(metadata_name, data_name):
            if data:
                print("    {}: {}".format(metadata_name, data[data_name]))
            else:
                if metadata_name in metadata:
                    print("    {}: {}".format(metadata_name, str(metadata[metadata_name])))
                not_in_dodson.add(lexeme)

    return (missing_in_dodson, twice_in_dodson)

def dump_missing(f, missing, known_missing):
    print("missing", file=f)
    for word in missing:
        if word not in known_missing:
            print("\t", word, file=f)
    print("{}".format(len(missing)), file=f)

def dump_twice(f, twice, known_twice):
    print("twice", file=f)
    for word in twice:
        if word not in known_twice:
            print("\t", word, file=f)
    print("{}".format(len(twice)), file=f)


OVERRIDABLE_METADATA_NAMES = ["dodson-entry",
                              "strongs",
                              "gk",
                              "gloss"]


argparser = argparse.ArgumentParser()
argparser.add_argument("dodson", type=argparse.FileType('r', encoding='UTF-8'), help="input dodson file")
argparser.add_argument("lexemes", help="input lexemes file")
argparser.add_argument("--missing", help="input file of words of the lexemes file known to be missing in dodson")
argparser.add_argument("--twice", help="input file of words of the lexemes file known to be present more than once in dodson")
argparser.add_argument("--override", choices=OVERRIDABLE_METADATA_NAMES, help="name of word metadata, as per lexemes file, for which the value in the dodson file shall be preferred to the value - if any - in the lexemes file")
argparser.add_argument("--output_lexemes", type=argparse.FileType('w', encoding='UTF-8'), default=sys.stdout, help="ouput lexemes file, equal to the input lexemes file enriched with information from input dodson file")
argparser.add_argument("--output_missing", type=argparse.FileType('w', encoding='UTF-8'), default=sys.stderr, help="output file of words of the lexemes file missing in dodson, and not known as such beforehand")
argparser.add_argument("--output_twice", type=argparse.FileType('w', encoding='UTF-8'), default=sys.stderr, help="input file of words of the lexemes file present more than once in dodson, and not known as such beforehand")

args = argparser.parse_args()
dodson = load_dodson(args.dodson)
lexemes = load_yaml(args.lexemes)
known_missing_in_dodson = load_wordset(args.missing) if args.missing else set()
known_twice_in_dodson = load_wordset(args.twice) if args.twice else set()
overrides = set(args.override)
output_file_lexemes = args.output_lexemes
output_file_missing_dodson = args.output_missing
output_file_twice_dodson = args.output_twice


(missing_in_dodson, twice_in_dodson) = dump_lexemes(output_file_lexemes, lexemes, dodson, overrides)
dump_missing(output_file_missing_dodson, missing_in_dodson, known_missing_in_dodson)
dump_twice(output_file_twice_dodson, twice_in_dodson, known_twice_in_dodson)
