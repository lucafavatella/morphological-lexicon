#!/usr/bin/env python3

import csv
import sys

import beta_to_unicode

def b2u(b):
    """See https://github.com/cltk/cltk/blob/v0.1.46/docs/greek.rst#converting-beta-code-to-unicode"""
    return beta_to_unicode.Replacer().beta_code(b)

csv_in = csv.DictReader(sys.stdin,
                        dialect='excel-tab',
                        strict=True)
csv_out = csv.DictWriter(sys.stdout, csv_in.fieldnames,
                         dialect='excel-tab',
                         quoting=csv.QUOTE_ALL, strict=True)

csv_out.writeheader()
for row in csv_in:
    csv_out.writerow(
        {f: (b2u(v.upper()) if f == "Greek Word" else v)
         for (f, v) in row.items()})
