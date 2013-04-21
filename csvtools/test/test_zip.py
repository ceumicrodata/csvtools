import unittest
from csvtools.test import ReaderWriter
import csvtools.zip as m


def csv_in(content):
    import csv
    from StringIO import StringIO
    import textwrap
    return csv.reader(StringIO(textwrap.dedent(content)))


class TestZip(unittest.TestCase):

    def test_normal_case(self):
        csv_in1 = csv_in('''\
            a,b,id
            a,b,1
            aa,bb,2''')
        csv_in2 = csv_in('''\
            c,d,id
            c,d,1
            cc,dd,2''')
        csv_out = ReaderWriter()

        m.csvzip(csv_in1, csv_in2, csv_out)

        self.assertEqual(3, len(csv_out.rows))
        self.assertEqual('a b c d'.split(), csv_out.rows[0])
        self.assertEqual('a b c d'.split(), csv_out.rows[1])
        self.assertEqual('aa bb cc dd'.split(), csv_out.rows[2])

    def test_keep_id_id_field_is_in_output(self):
        csv_in1 = csv_in('''\
            a,b,id
            a,b,1
            aa,bb,2''')
        csv_in2 = csv_in('''\
            c,d,id
            c,d,1
            cc,dd,2''')
        csv_out = ReaderWriter()

        m.csvzip(csv_in1, csv_in2, csv_out, keep_id=True)

        self.assertEqual(3, len(csv_out.rows))
        self.assertEqual('id a b c d'.split(), csv_out.rows[0])
        self.assertEqual('1 a b c d'.split(), csv_out.rows[1])
        self.assertEqual('2 aa bb cc dd'.split(), csv_out.rows[2])

    def test_no_common_field_zip_raises_error(self):
        csv_in1 = csv_in('a,b')
        csv_in2 = csv_in('c,d')
        csv_out = ReaderWriter()
        with self.assertRaises(m.BadInput):
            m.csvzip(csv_in1, csv_in2, csv_out)

    def test_two_common_fields_zip_raises_error(self):
        csv_in1 = csv_in('a,b')
        csv_in2 = csv_in('a,b')
        csv_out = ReaderWriter()
        with self.assertRaises(m.BadInput):
            m.csvzip(csv_in1, csv_in2, csv_out)

    def test_id_field_is_not_in_output(self):
        csv_in1 = csv_in('a,b,id')
        csv_in2 = csv_in('c,d,id')
        csv_out = ReaderWriter()

        m.csvzip(csv_in1, csv_in2, csv_out)

        self.assertNotIn('id', csv_out.rows[0])

    def test_mismatch_in_id_values_raises_error(self):
        csv_in1 = csv_in('''\
            a,b,id
            a,b,1
            aa,bb,2''')
        csv_in2 = csv_in('''\
            c,d,id
            c,d,1
            cc,dd,3''')
        csv_out = ReaderWriter()

        with self.assertRaises(m.IdMismatch):
            m.csvzip(csv_in1, csv_in2, csv_out)

        self.assertEqual(2, len(csv_out.rows))
        self.assertEqual('a b c d'.split(), csv_out.rows[0])
        self.assertEqual('a b c d'.split(), csv_out.rows[1])
