# coding: utf-8

import csv
import sys

"""
joins csv1 and csv2 .csv files on fields join_field. left join.

usage:
python simple_joiner.py csv1.csv csv2.csv out_csv.csv join_field1 [join_field2,
 ...]
"""


def get_indices(header, fields):
    return [header.index(field) for field in fields]


def make_picker(indices):
    def pick(item):
        return [item[index] for index in indices]
    return pick


def list_difference(list1, list2):
    return [x for x in list1 if x not in list2]


def list_intersection(list1, list2):
    return [x for x in list1 if x in list2]


def create_join_header(header1, header2, on_fields, suffix1='_1',
                       suffix2='_2'):
    # determine common fields
    common_fields = list_intersection(header1, header2)
    common_fields_no_join = list_difference(common_fields, on_fields)
    fields_only1 = list_difference(header1, common_fields)
    fields_only2 = list_difference(header2, common_fields)
    fields_common1 = [field + suffix1 for field in common_fields_no_join]
    fields_common2 = [field + suffix2 for field in common_fields_no_join]

    join_header = (
        fields_only1 + fields_common1 + on_fields
        + fields_only2 + fields_common2
    )

    pick_key_1 = make_picker(get_indices(header1, on_fields))
    pick_key_2 = make_picker(get_indices(header2, on_fields))
    pick_content_1 = make_picker(
        get_indices(header1, fields_only1 + common_fields_no_join + on_fields)
    )
    pick_content_2 = make_picker(
        get_indices(header2, fields_only2 + common_fields_no_join)
    )

    return join_header, pick_key_1, pick_key_2, pick_content_1, pick_content_2


def join_lists(iter1, iter2, on_fields):

    def joined_items(item1, item2):
        return (pick_content_1(item1) + pick_content_2(item2))

    def joined_items_if_null(item1):
        return (
            pick_content_1(item1)
            + [None] * (len(join_header) - len(pick_content_1(item1)))
        )

    iter1 = iter(iter1)
    list2 = list(iter2)

    header1 = iter1.next()
    header2 = list2[0]

    (join_header,
     pick_key_1,
     pick_key_2,
     pick_content_1,
     pick_content_2) = create_join_header(header1, header2, on_fields)
    yield join_header

    for item1 in iter1:
        match_found = False
        for item2 in iter(list2):
            if pick_key_1(item1) == pick_key_2(item2):
                match_found = True
                yield joined_items(item1, item2)
        if not match_found:
            yield joined_items_if_null(item1)


def join_csvs(in_csv1_path, in_csv2_path, out_csv_path, on_fields):
    with open(in_csv1_path, 'rb') as csv1:
        with open(in_csv2_path, 'rb') as csv2:
            with open(out_csv_path, 'wb') as outfile:
                reader_csv1 = csv.reader(csv1)
                reader_csv2 = csv.reader(csv2)
                outcsv = csv.writer(outfile)
                outcsv.writerows(join_lists(reader_csv1,
                                 reader_csv2, on_fields))


if __name__ == "__main__":
    join_csvs(
        in_csv1_path=sys.argv[1],
        in_csv2_path=sys.argv[2],
        out_csv_path=sys.argv[3],
        on_fields=sys.argv[4:]
    )
