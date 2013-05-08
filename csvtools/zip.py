import os
import sys
import csv

import argparse
import itertools
from lib import Header


class BadInput(Exception):
    pass


class IdMismatch(Exception):
    pass


def get_id_field(header1, header2):
    fields1 = set(header1)
    fields2 = set(header2)
    common_fields = fields1.intersection(fields2)

    if len(common_fields) != 1:
        raise BadInput

    id_field = common_fields.pop()
    return id_field


def extractors(header, excluded_field):
    return [
        header.extractor(field)
        for field in header
        if field != excluded_field]


def csvzip(csv_in1, csv_in2, csv_out, keep_id=False):
    i_csv_in1 = iter(csv_in1)
    i_csv_in2 = iter(csv_in2)

    header1 = Header(i_csv_in1.next())
    header2 = Header(i_csv_in2.next())

    id_field = get_id_field(header1, header2)

    id_extractor1 = header1.extractor(id_field)
    id_extractor2 = header2.extractor(id_field)

    output_extractors1 = extractors(header1, id_field)
    output_extractors2 = extractors(header2, id_field)

    def extract(extractors, row):
        return [extractor(row) for extractor in extractors]

    def zip_rows(row1, row2):
        zip_id1 = id_extractor1(row1)
        zip_id2 = id_extractor2(row2)
        if zip_id1 != zip_id2:
            raise IdMismatch

        output = (
            extract(output_extractors1, row1)
            + extract(output_extractors2, row2))

        if keep_id:
            return [zip_id1] + output
        else:
            return output

    csv_out.writerow(zip_rows(list(header1), list(header2)))
    for row1, row2 in itertools.izip(i_csv_in1, i_csv_in2):
        csv_out.writerow(zip_rows(row1, row2))


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--keep-id', action='store_true', dest='keep_id', default=False,
        help='keep id field in output')
    parser.add_argument(
        '--rm', action='store_true', dest='remove_input_file', default=False,
        help='remove input file (clean up when used in pipe)')
    parser.add_argument(
        'other_filename',
        help='other filename to zip with')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    csv_in1 = csv.reader(sys.stdin)
    csv_out = csv.writer(sys.stdout)

    with open(args.other_filename) as other_csv:
        csv_in2 = csv.reader(other_csv)

        csvzip(
            csv_in1, csv_in2, csv_out, keep_id=args.keep_id)

    if args.remove_input_file:
        os.remove(args.other_filename)


if __name__ == '__main__':
    main()
