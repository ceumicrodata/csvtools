# coding: utf-8

import sys
import csv


def csv_reader():
    return csv.reader(sys.stdin)


def pad(items, width):
    def fixed_width(item):
        if len(item) > width:
            raise ValueError(
                "Item has more than {width} elements: {item}"
                .format(width=width, item=item)
            )
        else:
            return item + [None] * (width - len(item))

    for item in items:
        yield fixed_width(item)


def print_as_csv(items):
    return (
        csv
        .writer(sys.stdout)
        .writerows(items)
    )


if __name__ == "__main__":
    width = int(sys.argv[1])

    print_as_csv(
        pad(csv_reader(), width)
    )
