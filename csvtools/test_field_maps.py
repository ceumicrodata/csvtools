import unittest
import csvtools.field_maps as m


class Test_FieldMaps_parse_from(unittest.TestCase):

    def test_only_one_output_field_input_defaults_to_output(self):
        fm = m.FieldMaps()

        fm.parse_from('out')

        self.assertEqual((('out', 'out'),), tuple(fm))

    def test_only_one_output_and_input_field(self):
        fm = m.FieldMaps()

        fm.parse_from('out=in')

        self.assertEqual((('out', 'in'),), tuple(fm))

    def test_two_fields(self):
        fm = m.FieldMaps()

        fm.parse_from('out1=in1,out2=in2')

        self.assertEqual((('out1', 'in1'), ('out2', 'in2')), tuple(fm))


