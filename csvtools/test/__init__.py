import csv
from StringIO import StringIO
import textwrap

import contextlib
import os
import sys


def csv_reader(content):
    return csv.reader(StringIO(textwrap.dedent(content)))


class ReaderWriter(object):

    '''
    Drop in replacement for both csv.reader and csv.writer
    '''

    rows = None

    def __init__(self):
        self.rows = []

    def writerow(self, row):
        self.rows.append(row)

    def writerows(self, rows):
        self.rows.extend(rows)

    def __iter__(self):
        return iter(self.rows)


@contextlib.contextmanager
def hide_stderr():
    '''
    Drop all output to stderr within block
    '''
    stderr = sys.stderr
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = stderr
