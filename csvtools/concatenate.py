import argparse
import csv
import sys
from StringIO import StringIO
import shutil


class InconsistentHeadersError(Exception):
    'Headers do not match'


class CsvAppender(object):

    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.header = None

    def append(self, stream):
        # write/check header
        line = stream.readline()
        header = iter(csv.reader(StringIO(line))).next()
        if self.header is None:
            self.header = header
            self.output_stream.write(line)
        elif header != self.header:
            raise InconsistentHeadersError(self.header, header)

        # copy rest of csv
        shutil.copyfileobj(stream, self.output_stream)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Concatenate csv files to stdout',
    )
    parser.add_argument(
        'filenames',
        metavar='FILE',
        nargs='+',
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    appender = CsvAppender(sys.stdout)

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
