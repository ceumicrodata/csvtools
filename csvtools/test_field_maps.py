import unittest
import csvtools.field_maps as m


def fm2out_in(fm):
    return tuple((f.output_field_name, f.input_field_name) for f in fm)

class Test_FieldMaps_parse_from(unittest.TestCase):

    def test_only_one_output_field_input_defaults_to_output(self):
        fm = m.FieldMaps()

        fm.parse_from('out')

        self.assertEqual((('out', 'out'),), fm2out_in(fm))

    def test_only_one_output_and_input_field(self):
        fm = m.FieldMaps()

        fm.parse_from('out=in')

        self.assertEqual((('out', 'in'),), fm2out_in(fm))

    def test_two_fields(self):
        fm = m.FieldMaps()

        fm.parse_from('out1=in1,out2=in2')

        self.assertEqual((('out1', 'in1'), ('out2', 'in2')), fm2out_in(fm))


class Test_field_maps_output_field_names(unittest.TestCase):

    def test(self):
        fm =m.FieldMaps()
        fm.parse_from('out1=in1,a,b')
        self.assertEqual(('out1', 'a', 'b'), fm.output_field_names)


class Test_SimpleTransformer_input_field_names(unittest.TestCase):

    def test(self):
        fm =m.FieldMaps()
        fm.parse_from('out1=in1,a,b')
        self.assertEqual(('in1', 'a', 'b'), fm.input_field_names)
