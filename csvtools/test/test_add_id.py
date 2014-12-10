#

import unittest

import csvtools.add_id as m


class Test_add_id(unittest.TestCase):

    def test_adds_header_and_starts_with_one(self):
        input_items = [
            ["a", "b"],
            ["lorem", "ipsum"],
            ["dolor", "sit"]
        ]

        output_items = [
            ["id", "a", "b"],
            [1, "lorem", "ipsum"],
            [2, "dolor", "sit"]
        ]

        self.assertEqual(
            list(m.add_id(input_items, "id")),
            output_items
        )
