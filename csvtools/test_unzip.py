import unittest
from csvtools.test import ReaderWriter
import csvtools.unzip as m


class TestUnzip(unittest.TestCase):

    def test_out_spec(self):
        csv_in = ReaderWriter()
        csv_in.writerow('a  b  c'.split())
        csv_in.writerow('a1 b1 c1'.split())
        csv_in.writerow('a2 b2 c2'.split())
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        m.unzip(csv_in, ['a'], csv_out_spec, csv_out_unspec)

        self.assertListEqual(
            ['id a'.split(),
             '0  a1'.split(),
             '1  a2'.split()],
            csv_out_spec.rows)

    def test_out_unspec(self):
        csv_in = ReaderWriter()
        csv_in.writerow('a  b  c'.split())
        csv_in.writerow('a1 b1 c1'.split())
        csv_in.writerow('a2 b2 c2'.split())
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        m.unzip(csv_in, ['a'], csv_out_spec, csv_out_unspec)

        self.assertListEqual(
            ['id b  c'.split(),
             '0  b1 c1'.split(),
             '1  b2 c2'.split()],
            csv_out_unspec.rows)

    def test_zip_id_defaults_to_id(self):
        csv_in = self.csv_header_a_b_c()
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        m.unzip(csv_in, ['a'], csv_out_spec, csv_out_unspec)

        self.assertListEqual(['id b c'.split()], csv_out_unspec.rows)

    def csv_header_a_b_c(self):
        csv = ReaderWriter()
        csv.writerow('a b c'.split())
        return csv

    def test_custom_zip_id_in_out_spec(self):
        csv_in = self.csv_header_a_b_c()
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        m.unzip(
            csv_in, ['a'], csv_out_spec, csv_out_unspec,
            zip_field='zip_id')

        self.assertListEqual(['zip_id a'.split()], csv_out_spec.rows)

    def test_custom_zip_id_in_out_unspec(self):
        csv_in = self.csv_header_a_b_c()
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        m.unzip(
            csv_in, ['a'], csv_out_spec, csv_out_unspec,
            zip_field='zip_id')

        self.assertListEqual(['zip_id b c'.split()], csv_out_unspec.rows)

    def test_input_contain_zip_field_exception(self):
        csv_in = self.csv_header_a_b_c()
        csv_out_spec = ReaderWriter()
        csv_out_unspec = ReaderWriter()

        with self.assertRaises(m.DuplicateFieldError):
            m.unzip(csv_in, ['a'], csv_out_spec, csv_out_unspec, zip_field='a')
