# coding: utf-8
'''
Filter input records and keep only those that covers the user specified
snapshot date.


TODO: supporting tools
- add a constant field to all rows (e.g. snapshot_date or snapshot_year)
- check the output for duplicate records within groups
  defined by a set of [key-] fields
  - keep the first from every group
  - add a new field containing the # of items in a group
    (e.g. snapshot_alternatives)
    it is characteristic quality of input data, and having higher than 1
    marks potential problem areas in input data.
'''

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


from argparse import ArgumentParser
from aniso8601 import parse_date

from datetime import date
from functools import partial
import operator
import sys
import unicodecsv


iso8601_date = parse_date


def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument(
        'from_field',
        help='start of interval field'
    )
    parser.add_argument(
        'to_field',
        help='end of interval field'
    )
    parser.add_argument(
        'snapshot_date',
        type=iso8601_date,
        help='snapshot date in YYYY-MM-DD format'
    )
    return parser.parse_args(argv)


def snapshot(rows, from_field, to_field, snapshot_date):
    irows = iter(rows)
    header = next(irows)
    yield header

    def get_date(row, get_field, default_date):
        try:
            return parse_date(get_field(row))
        except ValueError:
            return default_date
    get_from_date = partial(
        get_date,
        get_field=operator.itemgetter(header.index(from_field)),
        default_date=date.min
    )
    get_to_date = partial(
        get_date,
        get_field=operator.itemgetter(header.index(to_field)),
        default_date=date.max
    )

    for row in irows:
        from_date = get_from_date(row)
        to_date = get_to_date(row)
        if from_date <= snapshot_date < to_date:
            yield row


def main():
    args = parse_args(sys.argv[1:])
    unicodecsv.writer(sys.stdout).writerows(
        snapshot(
            unicodecsv.reader(sys.stdin),
            args.from_field, args.to_field, args.snapshot_date
        )
    )
