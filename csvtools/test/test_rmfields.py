import unittest
from mock import sentinel
import csvtools.rmfields as m
from csvtools.test import ReaderWriter


class Test_RemoveFields(unittest.TestCase):

    def test(self):
        reader = ReaderWriter()
        reader.rows = [
            ('aa', 'bb', 'cc', 'dd'),
            (sentinel.aa1, sentinel.bb1, sentinel.cc1, sentinel.dd1),
            (sentinel.aa2, sentinel.bb2, sentinel.cc2, sentinel.dd2), ]
        writer = ReaderWriter()

        m.RemoveFields(['cc', 'aa']).process(reader, writer)

        self.assertEqual(
            [
                ('bb', 'dd'),
                (sentinel.bb1, sentinel.dd1),
                (sentinel.bb2, sentinel.dd2),
            ],
            writer.rows)
