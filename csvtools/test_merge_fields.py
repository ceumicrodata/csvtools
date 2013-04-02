#

import unittest

import csvtools.merge_fields as m


class Test_merge_fields(unittest.TestCase):
    @property
    def input_items(self):
        return [["a", "b", "c"],
                ["lorem", "ipsum", "dolor"],
                ["sit", "amet", "consectetuer"]]

    def test_merge_single_column(self):
        self.assertEqual(
            list(m.merge_fields(
                    self.input_items,
                    constituents=["a"],
                    new_fieldname="d")),
            [["b", "c", "d"],
             ["ipsum", "dolor", "lorem"],
             ["amet", "consectetuer", "sit"]])

    def test_merge_multiple_columns(self):
        self.assertEqual(
            list(m.merge_fields(
                    self.input_items,
                    constituents=["a", "b"],
                    new_fieldname="d")),
            [["c", "d"],
             ["dolor", "lorem ipsum"],
             ["consectetuer", "sit amet"]])

