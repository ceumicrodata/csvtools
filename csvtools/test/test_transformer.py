import unittest
import mock
from mock import sentinel
from csvtools.test import ReaderWriter
import csvtools.transformer as m
from csvtools.field_maps import FieldMaps


class BindCheckerTransformer(m.Transformer):

    bound = False
    output_field_names = 'output_field_names'

    def bind(self, header):
        self.bound = True

    def transform(self, row):
        if not self.bound:
            raise Exception
        return row


class Test_Transformer_process(unittest.TestCase):

    def test_calls_bind_before_transform(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), (1, 2)]
        writer = ReaderWriter()

        BindCheckerTransformer().process(reader, writer)

    def test_header_is_output_field_names(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b')]
        writer = ReaderWriter()

        t = m.Transformer()
        t.output_field_names = sentinel.output_field_names

        t.process(reader, writer)

        self.assertEqual([sentinel.output_field_names], writer.rows)

    def test_content_is_produced_by_process(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), (1, 2), (1, 2)]
        writer = ReaderWriter()

        t = m.Transformer()
        t.transform = mock.Mock(t.transform, return_value=sentinel.output)

        t.process(reader, writer)

        self.assertEqual([sentinel.output, sentinel.output], writer.rows[1:])


def simple_transformer(field_maps_string):
    field_maps = FieldMaps()
    field_maps.parse_from(field_maps_string)
    return m.SimpleTransformer(field_maps)


class Test_SimpleTransformer_output_field_names(unittest.TestCase):

    def test(self):
        self.assertEqual(
            ('out1', 'a', 'b'),
            simple_transformer('out1=in1,a,b').output_field_names)


class Test_SimpleTransformer_input_field_names(unittest.TestCase):

    def test(self):
        self.assertEqual(
            ('in1', 'a', 'b'),
            simple_transformer('out1=in1,a,b').input_field_names)


class Test_SimpleTransformer_bind(unittest.TestCase):

    def test_sets_extractors(self):
        rb = simple_transformer('out1=in1,a,b')

        rb.bind(('a', 'in1', 'b'))

        self.assertEqual('in1', rb.extractors[0](('a', 'in1', 'b')))
        self.assertEqual('a', rb.extractors[1](('a', 'in1', 'b')))
        self.assertEqual('b', rb.extractors[2](('a', 'in1', 'b')))


class Test_SimpleTransformer_transform(unittest.TestCase):

    def test(self):
        header = ('a', 'aa', 'b', 'c')
        record = (sentinel.a, sentinel.aa, sentinel.b, sentinel.c)

        expected_transformed = (sentinel.c, sentinel.b, sentinel.aa)

        rb = simple_transformer('c,b,a=aa')

        rb.bind(header)

        self.assertEqual(expected_transformed, rb.transform(record))
