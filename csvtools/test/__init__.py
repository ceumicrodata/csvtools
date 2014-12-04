import csv
from StringIO import StringIO
import textwrap


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
