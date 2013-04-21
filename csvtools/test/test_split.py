import unittest

import os
from temp_dir import within_temp_dir

import codecs
import csv

from csvtools.test import ReaderWriter
import csvtools.split as m


def header(fname):
    with codecs.open(fname, encoding='utf8') as f:
        return f.readline().rstrip()


class Test_split(unittest.TestCase):

    @within_temp_dir
    def test_less_data_rows_than_chunk_size_one_file_created(self):
        rows = ReaderWriter()
        rows.writerow(u'a b'.split())
        rows.writerow([1, 2])
        rows.writerow([3, 4])

        m.split(rows, prefix='split.', chunk_size=3)

        self.assertTrue(os.path.exists(u'split.0'))
        self.assertFalse(os.path.exists(u'split.1'))

    @within_temp_dir
    def test_11_data_rows_chunk_size_1_11_files_created(self):
        rows = ReaderWriter()
        rows.writerow(u'a b'.split())
        for i in range(11):
            rows.writerow([i, i+1])

        m.split(rows, prefix='split.', chunk_size=1)

        self.assertTrue(os.path.exists(u'split.0'))
        self.assertTrue(os.path.exists(u'split.1'))
        # ...
        self.assertTrue(os.path.exists(u'split.10'))
        self.assertFalse(os.path.exists(u'split.11'))

    @within_temp_dir
    def test_multiple_output_files_have_same_header(self):
        rows = ReaderWriter()
        rows.writerow(u'a b'.split())
        rows.writerow([1, 2])
        rows.writerow([3, 4])

        m.split(rows, prefix='split.', chunk_size=1)

        self.assertEqual(u'a,b', header(u'split.0'))
        self.assertEqual(u'a,b', header(u'split.1'))

    @within_temp_dir
    def test_header_only_input_one_output_file_with_header(self):
        rows = ReaderWriter()
        rows.writerow(u'a b'.split())

        m.split(rows, prefix='split.', chunk_size=1)

        self.assertEqual(u'a,b', header(u'split.0'))

    @within_temp_dir
    def test_output_file_contains_rows_from_input(self):
        rows = ReaderWriter()
        rows.writerow(u'a b'.split())
        rows.writerow([1, 2])
        rows.writerow([3, 4])

        m.split(rows, prefix='split.', chunk_size=2)

        with codecs.open('split.0', encoding='utf8') as f:
            self.assertEqual(
                [[u'a', u'b'],
                 [u'1', u'2'],
                 [u'3', u'4']],
                list(csv.reader(f)))
