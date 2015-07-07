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


from argparse import ArgumentParser, FileType
from aniso8601 import parse_date

from datetime import date
from functools import partial
import operator
import sys
import unicodecsv


iso8601_date = parse_date

def fix_win():
    # http://stackoverflow.com/questions/2374427/python-2-x-write-binary-output-to-stdout
    # http://code.activestate.com/recipes/65443-sending-binary-data-to-stdout-under-windows/
    if sys.platform == "win32":
        import os
        try:
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
            sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb')
        except:
            sys.stderr.write('Can not set stdout to binary.\n')

# "fix" win32 to provide binary stdout
fix_win()


def parse_args(argv):
    parser = ArgumentParser()
    arg = parser.add_argument
    arg('from_field', help='start of interval field')
    arg('to_field', help='end of interval field')
    arg('snapshot_date', type=iso8601_date,
        help='snapshot date in YYYY-MM-DD format')
    arg('--input', type=FileType('rb'), default=sys.stdin)
    arg('--output', type=FileType('wb'), default=sys.stdout)
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
        default_date=date.min)
    get_to_date = partial(
        get_date,
        get_field=operator.itemgetter(header.index(to_field)),
        default_date=date.max)

    for row in irows:
        from_date = get_from_date(row)
        to_date = get_to_date(row)
        if from_date <= snapshot_date < to_date:
            yield row


def main():
    args = parse_args(sys.argv[1:])
    input_csv = unicodecsv.reader(args.input)
    output_csv = unicodecsv.writer(args.output)
    output_csv.writerows(
        snapshot(
            input_csv, args.from_field, args.to_field, args.snapshot_date))
