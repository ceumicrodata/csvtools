import argparse
import csv
import sys


class InconsistentHeadersError(Exception):
    'Headers do not match'


class CsvAppender(object):

    def __init__(self, output_stream, max_csv_field_size):
        self.writer = csv.writer(output_stream)
        self.header = None
        csv.field_size_limit(max_csv_field_size)

    def append(self, stream):
        reader = iter(csv.reader(stream))
        header = reader.next()
        if self.header is None:
            self.header = header
            self.writer.writerow(header)
        elif header != self.header:
            raise InconsistentHeadersError(self.header, header)
        self.writer.writerows(reader)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Concatenate csv files',
    )
    parser.add_argument(
        'filenames',
        metavar='FILE',
        nargs='+',
    )
    parser.add_argument(
        '--max-csv-field-size',
        type=int,
        default=csv.field_size_limit(),
        help=(
            'CSV reader parameter, raise for very big text fields'
            + ' containing new lines (default %(default)s)'
        ),
    )
    parser.add_argument(
        '-p',
        '--progress',
        action='store_true',
        default=False,
        help='Show progress',
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    appender = CsvAppender(
        sys.stdout,
        max_csv_field_size=args.max_csv_field_size
    )

    for filename in args.filenames:
        with open(filename) as file:
            try:
                appender.append(file)
            except:
                sys.stderr.write(
                    'Exception in file >>> {} <<<\n'.format(filename)
                )
                raise


if __name__ == "__main__":
    main()
