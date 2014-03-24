# coding: utf-8

import sys
import csv


def read_csv():
    return csv.reader(sys.stdin)


def merge_fields(items, constituents, new_fieldname):
    items = iter(items)
    header = items.next()
    constituent_indices = list(index
                               for index, fieldname in enumerate(header)
                               if fieldname in constituents)
    other_indices = list(index
                         for index, fieldname in enumerate(header)
                         if fieldname not in constituents)

    def pick(elements, indices):
        return list(element
                    for index, element in enumerate(elements)
                    if index in indices)

    def constituent_values(item):
        return pick(item, constituent_indices)

    def new_item(item, new_field_value):
        return (pick(item, other_indices)
                + [new_field_value])

    yield new_item(header, new_fieldname)

    for item in items:
        yield new_item(item, " ".join(constituent_values(item)))


def print_as_csv(items):
    return (csv
            .writer(sys.stdout)
            .writerows(items))


if __name__ == "__main__":
    constituents = sys.argv[1].split(",")
    new_fieldname = sys.argv[2]

    print_as_csv(
        merge_fields(
            read_csv(),
            constituents,
            new_fieldname))
