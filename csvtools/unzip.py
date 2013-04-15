import argparse
from operator import itemgetter


class DuplicateFieldError(Exception):
    pass


def unzip(csv_in, fields, csv_out_spec, csv_out_unspec, zip_field='id'):
    input_csv = iter(csv_in)

    header = input_csv.next()
    extractors_by_name = dict(
        (header_field, itemgetter(i))
        for (i, header_field) in enumerate(header))

    if zip_field in extractors_by_name:
        raise DuplicateFieldError(zip_field)

    spec_extractors = [extractors_by_name[field] for field in fields]
    unspec_extractors = [
        extractors_by_name[field]
        for field in header
        if field not in fields]

    def extract_to(output, extractors, row_id, row):
        output.writerow(
            [str(row_id)]
            + [extract_field(row) for extract_field in extractors])

    def unzip_row(row_id, row):
        extract_to(csv_out_spec, spec_extractors, row_id, row)
        extract_to(csv_out_unspec, unspec_extractors, row_id, row)

    unzip_row(zip_field, header)
    for zip_id, row in enumerate(input_csv):
        unzip_row(zip_id, row)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--id', action='store', dest='zip_field', default='id',
        help='new field that matches rows in unzipped parts (%(default)s)')
    parser.add_argument(
        'fields', metavar='FIELDS',
        help='comma separated field names')
    parser.add_argument(
        'unspec_fields_filename', metavar='UNSPEC_FILENAME',
        help='Filename for unspecified fields')

    return parser.parse_args(args)


if __name__ == '__main__':
    import sys
    import csv

    args = parse_args(sys.argv[1:])

    fields = args.fields.split(',')
    csv_in = csv.reader(sys.stdin)
    csv_out_spec = csv.writer(sys.stdout)

    with open(args.unspec_fields_filename, 'w') as out_unspec:
        csv_out_unspec = csv.writer(out_unspec)

        unzip(
            csv_in, fields, csv_out_spec, csv_out_unspec,
            zip_field=args.zip_field)
