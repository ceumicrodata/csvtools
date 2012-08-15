#! -*- encoding: utf8 -*-
import unittest
import csvtools.select as m
from csvtools.test import ReaderWriter
from StringIO import StringIO
import csv


class Test_process(unittest.TestCase):

    def test_change_order(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), (1, 2)]
        writer = ReaderWriter()

        m.process(reader, writer, m.RecordTransformer('b,a'))

        self.assertEqual([('b', 'a'), (2, 1)], writer.rows)


class Test_select(unittest.TestCase):

    def test_change_order(self):
        input_file = StringIO(
            'a,b\n'
            '1,2')
        output_file = StringIO()

        m.select(input_file, output_file, 'b,a')

        r = csv.reader(StringIO(output_file.getvalue()))
        self.assertEqual(('b', 'a'), tuple(r.next()))
        self.assertEqual(('2', '1'), tuple(r.next()))

    def test_float(self):
        input_file = StringIO(
            'a,b\n'
            '1.2345678901000,2')
        output_file = StringIO()

        m.select(input_file, output_file, 'a,b')

        r = csv.reader(StringIO(output_file.getvalue()))
        self.assertEqual(('a', 'b'), tuple(r.next()))
        self.assertEqual(('1.2345678901000', '2'), tuple(r.next()))

    def test_utf8_input(self):
        input_file = StringIO(
            u'a,b\nárvíztűrőtükörfúrógép,2'.encode('utf8'))
        output_file = StringIO()

        m.select(input_file, output_file, 'a,b')

        r = csv.reader(StringIO(output_file.getvalue()))
        self.assertEqual(('a', 'b'), tuple(r.next()))
        self.assertEqual(('árvíztűrőtükörfúrógép', '2'), tuple(r.next()))
