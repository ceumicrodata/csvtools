import csv
import itertools
import optparse
import sys


def find_maximum(items, field, groupby=None):
    def group_key(item):
        if not groupby:
            return None
        else:
            return tuple(item.get(field) for field in groupby.split(","))

    def max_key(item):
        return float(item.get(field))

    for group_id, group in itertools.groupby(items, key=group_key):
        group = tuple(group)
        max_item = max(group, key=max_key)

        for item in group:
            if max_key(item) == max_key(max_item):
                yield item


def dump_as_csv(items):
    first_item = next(items)
    writer = csv.DictWriter(sys.stdout, fieldnames=first_item.keys())

    writer.writeheader()
    writer.writerow(first_item)
    writer.writerows(items)


if __name__ == "__main__":
    parser = optparse.OptionParser(
                usage="Usage: %prog [options] FIELDNAME",
                description=("Find maximum-value items."
                             + "  Input should be sorted by groups."))
    parser.add_option(
                "-g",
                "--groupby",
                dest="fieldnames",
                help="find maximum within groups defined by FIELDNAMES")

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("invalid number of arguments")

    dump_as_csv(
        find_maximum(
            csv.DictReader(sys.stdin),
            field=args[0],
            groupby=options.fieldnames))

