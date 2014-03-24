import unittest

import csvtools.sort as m


class Items(object):
    fieldnames = ["a", "b", "c"]

    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)


class Test_sort(unittest.TestCase):

    def test_non_numeric(self):
        self.assertEqual(
            list(
                m.sort(
                    Items(
                        [dict(a=1, b=3, c="1"),
                         dict(a=2, b=2, c="100"),
                         dict(a=3, b=1, c="12")]),
                    "b")),
            [["a", "b", "c"],
             [3, 1, "12"],
             [2, 2, "100"],
             [1, 3, "1"]])

        self.assertEqual(
            list(
                m.sort(
                    Items(
                        [dict(a=1, b=3, c="1"),
                         dict(a=2, b=2, c="100"),
                         dict(a=3, b=1, c="12")]),
                    "c")),
            [["a", "b", "c"],
             [1, 3, "1"],
             [2, 2, "100"],
             [3, 1, "12"]])

    def test_numeric(self):
        self.assertEqual(
            list(
                m.sort(
                    Items(
                        [dict(a=1, b=3, c="1"),
                         dict(a=2, b=2, c="100"),
                         dict(a=3, b=1, c="12")]),
                    "c",
                    numeric=True)),
            [["a", "b", "c"],
             [1, 3, "1"],
             [3, 1, "12"],
             [2, 2, "100"]])

