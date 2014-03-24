#

import unittest

import csvtools.pad as m


class Test_pad(unittest.TestCase):
    def test_leaves_proper_width_input_untouched(self):
        self.assertEqual(
            list(m.pad(
                    items=[["a", "b", "c"],
                           ["lorem", "ipsum", "dolor"]],
                    width=3)),
            [["a", "b", "c"],
             ["lorem", "ipsum", "dolor"]])

    def test_fixes_narrow_input(self):
        self.assertEqual(
            list(m.pad(
                    items=[["a", "b", "c"],
                           ["lorem", "ipsum"]],
                    width=3)),
            [["a", "b", "c"],
             ["lorem", "ipsum", None]])

    def test_raises_exception_on_wide_input(self):
        with self.assertRaises(ValueError):
            list(m.pad(
                    items=[["a", "b", "c"],
                           ["lorem", "ipsum", "dolor"]],
                    width=2))

