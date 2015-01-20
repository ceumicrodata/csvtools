import unittest

import csvtools.pad as m


class Test_pad(unittest.TestCase):

    def test_adds_header_and_starts_with_one(self):
        input_items = [
            ["a", "b", "c"],
            ["lorem", "ipsum"],
            ["dolor", "sit"]
        ]

        output_items = [
            ["a", "b", "c"],
            ["lorem", "ipsum", ""],
            ["dolor", "sit", ""]
        ]

        self.assertEqual(
            list(m.pad_csv(input_items)),
            output_items
        )
