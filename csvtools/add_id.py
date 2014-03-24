# coding: utf-8

import sys
import csv


def read_csv():
    return csv.reader(sys.stdin)


def add_id(items, id_fieldname):
    items = iter(items)

    def header():
        header = items.next()

        return [id_fieldname] + header

    yield header()

    for id, item in enumerate(items, 1):
        yield [id] + item


def print_as_csv(items):
    writer = csv.writer(sys.stdout)

    writer.writerows(items)


if __name__ == "__main__":
    try:
        id_fieldname = sys.argv[1]
    except IndexError:
        id_fieldname = "id"

    print_as_csv(
        add_id(
            read_csv(),
            id_fieldname))
