import unittest
import csvtools.lib as m


class TestHeader(unittest.TestCase):

    @property
    def header(self):
        return m.Header('a b c'.split())

    def test_len(self):
        self.assertEqual(3, len(self.header))

    def test_in(self):
        header = self.header
        self.assertTrue('a' in header)
        self.assertTrue('b' in header)
        self.assertTrue('c' in header)

    def test_not_in(self):
        self.assertTrue('d' not in self.header)

    def test_iter(self):
        self.assertEqual(['a', 'b', 'c'], list(self.header))

    def test_extractor(self):
        extractor = self.header.extractor('b')
        self.assertEqual(2, extractor([1, 2, 3]))
