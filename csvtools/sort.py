import csv
import optparse
import sys


def sort(items, fields, numeric=False):
    def key(item):
        return tuple(
            float(item.get(k)) if numeric else item.get(k)
            for k in fields
        )

    def ordered(item):
        return list(item.get(k) for k in items.fieldnames)

    yield items.fieldnames

    for item in sorted(items, key=key):
        yield ordered(item)


def dump_as_csv(items):
    return (
        csv
        .writer(sys.stdout)
        .writerows(items)
    )


if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="Usage: %prog [options] FIELDNAMES",
        description="Sort items by FIELDNAMES."
    )
    parser.add_option(
        "-n",
        "--numeric-sort",
        action="store_true",
        default=False,
        dest="numeric",
        help="compare according to numerical value"
    )

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("invalid number of arguments")

    dump_as_csv(
        sort(
            csv.DictReader(sys.stdin),
            fields=args[0].split(","),
            numeric=options.numeric
        )
    )
