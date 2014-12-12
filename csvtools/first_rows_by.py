# coding: utf-8
'''
Keep first elements of groups, with group size.

This is for working with dirty data and marking problem spots,
where we have more observations than the expected one.

NOTE: Groups are created from a streaming data,
so data having the same keys are expected to be adjecent
(data is sorted by the given key).

csv_first_rows_by [--group-size-field=group_size] key-fields

'''

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import csv
import sys
import itertools
import operator


def first_rows_by(rows, group_fields, group_size_field):
    irows = iter(rows)
    header = next(irows)
    get_key = operator.itemgetter(*[header.index(f) for f in group_fields])

    assert group_size_field not in header
    yield header + [group_size_field]
    for key, igroup in itertools.groupby(rows, get_key):
        group = list(igroup)
        yield group[0] + [len(group)]


def main():
    writer = csv.writer(sys.stdout)
    writer.writerows(
        first_rows_by(
            rows=csv.reader(sys.stdin),
            group_fields=sys.argv[1:],
            group_size_field='group_size',
        )
    )
