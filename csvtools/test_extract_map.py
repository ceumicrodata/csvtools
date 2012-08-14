import unittest
import mock
import csvtools.extract_map as m


def mmap():
    # mocked out Map - will not write to fs
    map = m.Map('asd.csv', '', 'id')
    map.write = mock.Mock()
    return map


class Test_Map_add(unittest.TestCase):

    def test_add_marks_map_modified(self):
        map = mmap()

        map.add(tuple())

        self.assertTrue(map.modified)

    def test_next_ref_incremented(self):
        map = mmap()

        next_ref = map.next_ref

        map.add(tuple())

        self.assertEqual(next_ref + 1, map.next_ref)


class Test_Map_field_names(unittest.TestCase):

    def test(self):
        map = m.Map('asd.csv', 'a,b', 'id')

        self.assertEqual(set(('a', 'b', 'id')), set(map.field_names))


class Test_Map_bind(unittest.TestCase):

    def test_binds_the_internal_transformer(self):
        map = m.Map('asd.csv', 'a,b', 'id')

        map.bind(('a', 'b', 'c'))

        self.assertEqual(('a', 'b'), map.transformer.transform(('a', 'b', 'c')))
