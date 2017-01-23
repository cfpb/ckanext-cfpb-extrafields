"""
Extract fields from an excel file and print the results.

Useful for testing the behavior of dig import without running CKAN.
"""
from __future__ import print_function
import sys
import pprint

from ckanext.cfpb_extrafields.digutils import make_rec

def main(args):
    if len(args) == 2 and args[1] not in ["-h", "--help", "help"]:
        with open(args[1], "r") as dig_file:
            result = make_rec(dig_file)
            pprint.pprint(result)
    else:
        print("usage: python tst_import.py <dig_file>")

if __name__ == "__main__":
    main(sys.argv)
