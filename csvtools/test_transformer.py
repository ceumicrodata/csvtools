import unittest
import mock
from mock import sentinel
from csvtools.test import ReaderWriter
import csvtools.transformer as m


class BindCheckerTransformer(m.Transformer):

    bound = False
    output_header = 'output_header'

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

    def test_header_is_output_header(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b')]
        writer = ReaderWriter()

        t = m.Transformer()
        t.output_header = sentinel.output_header

        t.process(reader, writer)

        self.assertEqual([sentinel.output_header], writer.rows)

    def test_content_is_produced_by_process(self):
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), (1, 2), (1, 2)]
        writer = ReaderWriter()

        t = m.Transformer()
        t.transform = mock.Mock(t.transform, return_value=sentinel.output)

        t.process(reader, writer)

        self.assertEqual([sentinel.output, sentinel.output], writer.rows[1:])


class Test_RecordTransformer_parse_transformer_spec_string(unittest.TestCase):

    def test_only_one_output_field_input_defaults_to_output(self):
        rb = m.RecordTransformer('')
        self.assertEqual((('out', 'out'),), rb.parse_transformer_spec_string('out'))

    def test_only_one_output_and_input_field(self):
        rb = m.RecordTransformer('')
        self.assertEqual((('out', 'in'),), rb.parse_transformer_spec_string('out=in'))

    def test_two_fields(self):
        rb = m.RecordTransformer('')
        self.assertEqual((('out1', 'in1'), ('out2', 'in2')), rb.parse_transformer_spec_string('out1=in1,out2=in2'))


class Test_RecordTransformer_output_header(unittest.TestCase):

    def test(self):
        self.assertEqual(('out1', 'a', 'b'), m.RecordTransformer('out1=in1,a,b').output_header)


class Test_RecordTransformer_input_field_names(unittest.TestCase):

    def test(self):
        self.assertEqual(('in1', 'a', 'b'), m.RecordTransformer('out1=in1,a,b').input_field_names)


class Test_RecordTransformer_bind(unittest.TestCase):

    def test_sets_extractors(self):
        rb = m.RecordTransformer('out1=in1,a,b')

        rb.bind(('a', 'in1', 'b'))

        self.assertEqual('in1', rb.extractors[0](('a', 'in1', 'b')))
        self.assertEqual('a', rb.extractors[1](('a', 'in1', 'b')))
        self.assertEqual('b', rb.extractors[2](('a', 'in1', 'b')))


class Test_RecordTransformer_transform(unittest.TestCase):

    def test(self):
        header = ('a', 'aa', 'b', 'c')
        record = (sentinel.a, sentinel.aa, sentinel.b, sentinel.c)

        expected_transformed = (sentinel.c, sentinel.b, sentinel.aa)

        rb = m.RecordTransformer('c,b,a=aa')

        rb.bind(header)

        self.assertEqual(expected_transformed, rb.transform(record))
