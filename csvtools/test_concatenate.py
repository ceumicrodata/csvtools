# coding: utf-8

import unittest
from StringIO import StringIO
import csv
import csvtools.concatenate as m


def csv_rows(string_io):
    return list(csv.reader(StringIO(string_io.getvalue())))


class Test_concatenate(unittest.TestCase):
    @property
    def input_a(self):
        return StringIO("id,lorem,ipsum\n"
                        "1,dolor,sit\n"
                        "2,amet,consectetuer")
    @property
    def input_b(self):
        return StringIO("id,lorem,ipsum\n"
                        "3,adipisicing,velit")

    @property
    def input_c(self):
        return StringIO("id\n"
                        "4\n"
                        "5")

    def test_single_input_returned(self):
        output = StringIO()

        m.concatenate((self.input_a,), output)

        self.assertEqual(csv_rows(output),
                         [["id", "lorem", "ipsum"],
                          ["1", "dolor", "sit"],
                          ["2", "amet", "consectetuer"]])

    def test_two_inputs_concatenated(self):
        output = StringIO()

        m.concatenate((self.input_a,
                       self.input_b),
                      output)

        self.assertEqual(csv_rows(output),
                         [["id", "lorem", "ipsum"],
                          ["1", "dolor", "sit"],
                          ["2", "amet", "consectetuer"],
                          ["3", "adipisicing", "velit"]])

    def test_inconsistent_fieldnames_not_accepted(self):
        output = StringIO()

        with self.assertRaises(m.InconsistentHeadersError):
            m.concatenate((self.input_a,
                           self.input_b,
                           self.input_c),
                          output)

