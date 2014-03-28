# Py3 compatibility
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys

if sys.version_info.major == 2:
    import codecs
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)


class InconsistentHeadersError(Exception):
    'Headers do not match'


class CsvAppender(object):

    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.header = None

    def append(self, stream):
        # write/check header
        lines = (line.rstrip('\n') for line in stream)
        header = next(lines)
        if self.header is None:
            self.header = header
            self.output_stream.write(header)
            self.output_stream.write('\n')
        elif header != self.header:
            raise InconsistentHeadersError(self.header, header)

        # copy rest of csv
        for line in lines:
            self.output_stream.write(line)
            self.output_stream.write('\n')


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
        with io.open(filename, 'rtU') as file:
            try:
                appender.append(file)
            except:
                sys.stderr.write(
                    'Exception in file >>> {} <<<\n'.format(filename)
                )
                raise


if __name__ == "__main__":
    main()
