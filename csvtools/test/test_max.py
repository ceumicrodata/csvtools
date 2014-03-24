import unittest

import csvtools.max as m


class Items(object):
    fieldnames = ["a", "b"]

    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)


class Test_max(unittest.TestCase):

    def test_without_groupby(self):
        self.assertEqual(
            list(
                m.find_maximum(
                    Items(
                        [dict(a=1, b="0.1"),
                         dict(a=1, b="0.9"),
                         dict(a=1, b="0.9"),
                         dict(a=2, b="0.8")]),
                    "b")),
            [["a", "b"],
             [1, "0.9"],
             [1, "0.9"]])

    def test_with_groupby(self):
        self.assertEqual(
            list(
                m.find_maximum(
                    Items(
                        [dict(a=1, b="0.1"),
                         dict(a=1, b="0.9"),
                         dict(a=1, b="0.9"),
                         dict(a=2, b="0.8")]),
                    "b",
                    groupby=["a"])),
            [["a", "b"],
             [1, "0.9"],
             [1, "0.9"],
             [2, "0.8"]])
