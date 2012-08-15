import unittest
from mock import sentinel
import csvtools.field as m


class Test_NamedField_bind(unittest.TestCase):

    def test_index_of_name_stored(self):
        f = m.NamedField('name')

        f.bind(('a', 'b', 'name', 'c'))

        self.assertEqual(2, f.index)

    def test_makes_field_bound(self):
        f = m.NamedField('name')

        f.bind(('a', 'b', 'name', 'c'))

        self.assertTrue(f.bound)


class Test_NamedField_value_extractor(unittest.TestCase):

    def test_existing_field(self):
        f = m.NamedField('name')
        f.index = 1

        self.assertEqual(sentinel.second, f.value_extractor((sentinel.first, sentinel.second, sentinel.third)))

    def test_nonexisting_field(self):
        f = m.NamedField('name')
        f.index = None

        self.assertIsNone(f.value_extractor((sentinel.first, sentinel.second)))
