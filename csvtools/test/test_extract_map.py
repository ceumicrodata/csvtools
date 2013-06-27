import unittest
import mock
from mock import sentinel
from temp_dir import within_temp_dir
import csv

from csvtools.test import ReaderWriter
from csvtools.field_maps import FieldMaps
import csvtools.extract_map as m


def make_map(field_maps_spec, ref_field_name):
    field_maps = FieldMaps()
    field_maps.parse_from(field_maps_spec)
    return m.Map(field_maps, ref_field_name)


class Test_Map_field_names(unittest.TestCase):

    def test(self):
        map = make_map('a,b', 'id')

        self.assertEqual(set(('a', 'b', 'id')), set(map.field_names))


class Test_Map_bind(unittest.TestCase):

    def test_binds_the_internal_transformer(self):
        map = make_map('a,b', 'id')

        map.bind(('a', 'b', 'c'))

        self.assertEqual(
            ('a', 'b'), map.transformer.transform(('a', 'b', 'c')))


class Test_Map_translate(unittest.TestCase):

    def test_uses_internal_transformer(self):
        map = make_map('aa,bb', 'id')
        map.transformer = mock.Mock()
        map.transformer.transform = (
            mock.Mock(return_value=(sentinel.aa1, sentinel.bb1)))

        map.values = {
            (sentinel.aa1, sentinel.bb1): sentinel.ref1,
        }

        input_row = ('prefix', sentinel.bb1, 'middle', sentinel.aa1, 'suffix')
        ref = map.translate(input_row)

        map.transformer.transform.assert_called_once_with(input_row)
        self.assertEqual(sentinel.ref1, ref)

    def fixture_aa_bb_with_aa1_bb1_1(self):
        map = make_map('aa,bb', 'id')
        map.bind(('aa', 'bb'))

        map.values = {
            (sentinel.aa1, sentinel.bb1): 1,
        }
        map.next_ref = 2

        return map

    def test_if_not_in_values_adds_new_value(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()

        map.translate((sentinel.aa_notin, sentinel.bb_notin))

        self.assertEqual(
            {
                (sentinel.aa1, sentinel.bb1): 1,
                (sentinel.aa_notin, sentinel.bb_notin): 2
            },
            map.values)

    def test_if_not_in_values_ref_returned_is_previous_next_ref(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()
        map.changed = False

        previous_next_ref = map.next_ref
        ref = map.translate((sentinel.aa_notin, sentinel.bb_notin))

        self.assertEqual(previous_next_ref, ref)

    def test_if_not_in_values_next_ref_is_incremented(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()
        map.changed = False

        previous_next_ref = map.next_ref
        map.translate((sentinel.aa_notin, sentinel.bb_notin))

        self.assertEqual(previous_next_ref + 1, map.next_ref)

    def test_if_not_in_values_sets_modified(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()
        map.changed = False

        map.translate((sentinel.aa_notin, sentinel.bb_notin))

        self.assertTrue(map.changed)

    def test_if_modified_and_in_values_remains_modified(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()
        map.changed = True

        map.translate((sentinel.aa1, sentinel.bb1))

        self.assertTrue(map.changed)

    def test_if_unmodified_and_in_values_remains_unmodified(self):
        map = self.fixture_aa_bb_with_aa1_bb1_1()
        map.changed = False

        map.translate((sentinel.aa1, sentinel.bb1))

        self.assertFalse(map.changed)

    def test_empty_map(self):
        map = make_map('aa', 'id')
        map.bind(['aa'])

        map.translate([sentinel.new])

        self.assertEqual({(sentinel.new,): 0}, map.values)


class Test_Map_write(unittest.TestCase):

    def test_header(self):
        map = make_map('aa,bb', 'id')

        writer = ReaderWriter()
        map.write(writer)

        self.assertEqual([('id', 'aa', 'bb')], writer.rows)

    def test_content(self):
        map = make_map('aa,bb', 'id')
        map.values = {
            (sentinel.aa1, sentinel.bb1): sentinel.ref1,
            (sentinel.aa2, sentinel.bb2): sentinel.ref2
        }

        writer = ReaderWriter()
        map.write(writer)

        self.assertEqual(
            sorted([
                (sentinel.ref1, sentinel.aa1, sentinel.bb1),
                (sentinel.ref2, sentinel.aa2, sentinel.bb2)]),
            sorted(writer.rows[1:]))


class Test_Map_read(unittest.TestCase):

    header = ('id', 'aa', 'bb')

    def write_aa1_aa2_88(self, writer):
        map = make_map('aa,bb', 'id')
        map.values = {
            (sentinel.aa1, sentinel.bb1): 88,
            (sentinel.aa2, sentinel.bb2): 19
        }
        map.write(writer)

    def test_values_read_back(self):
        rw = ReaderWriter()
        self.write_aa1_aa2_88(rw)

        newmap = make_map('aa,bb', 'id')
        newmap.read(rw)

        self.assertEqual(
            {
                (sentinel.aa1, sentinel.bb1): 88,
                (sentinel.aa2, sentinel.bb2): 19
            },
            newmap.values)

    def test_next_ref_is_set_to_maxref_plus_1(self):
        rw = ReaderWriter()
        self.write_aa1_aa2_88(rw)

        newmap = make_map('aa,bb', 'id')
        newmap.read(rw)

        self.assertEqual(89, newmap.next_ref)

    def test_fields_swapped_properly_reads_back(self):
        rw = ReaderWriter()
        self.write_aa1_aa2_88(rw)

        newmap = make_map('bb,aa', 'id')
        newmap.read(rw)

        self.assertEqual(
            {
                (sentinel.bb1, sentinel.aa1): 88,
                (sentinel.bb2, sentinel.aa2): 19
            },
            newmap.values)

    def test_ids_are_converted_to_string(self):
        rw = ReaderWriter()
        rw.rows = [('id', 'value'), ('1', 'one')]

        newmap = make_map('value', 'id')
        newmap.read(rw)

        self.assertEqual(
            {('one',): 1},
            newmap.values)

    def test_refs_not_unique_dies(self):
        reader = ReaderWriter()
        reader.rows = [self.header, (1, 1, 1), (1, 2, 2)]
        map = make_map('aa,bb', 'id')

        self.assertRaises(Exception, lambda: map.read(reader))

    def test_valuess_not_unique_dies(self):
        reader = ReaderWriter()
        reader.rows = [self.header, (1, 1, 1), (2, 1, 1)]
        map = make_map('aa,bb', 'id')

        self.assertRaises(Exception, lambda: map.read(reader))

    def test_missing_ref_field(self):
        reader = ReaderWriter()
        reader.rows = [('aa', 'bb')]
        map = make_map('aa,bb', 'id')

        self.assertRaises(Exception, lambda: map.read(reader))

    def test_missing_value_field(self):
        reader = ReaderWriter()
        reader.rows = [('id', 'bb')]
        map = make_map('aa,bb', 'id')

        self.assertRaises(Exception, lambda: map.read(reader))


class Test_RefField(unittest.TestCase):

    def test_ref(self):
        map = make_map('aamap=aamain,bbmap=bbmain', 'idmap')
        map.next_ref = 100
        f = m.RefField(map)
        f.bind(('aamain', 'bbmain', 'ccmain'))

        ref = f.value_extractor((sentinel.aa, sentinel.bb, sentinel.cc))

        self.assertEqual(100, ref)

    def test_map_content(self):
        map = make_map('aamap=aamain,bbmap=bbmain', 'idmap')
        map.next_ref = 100
        f = m.RefField(map)
        f.bind(('aamain', 'bbmain', 'ccmain'))

        f.value_extractor((sentinel.aa, sentinel.bb, sentinel.cc))

        writer = ReaderWriter()
        map.write(writer)
        self.assertEqual(
            [('idmap', 'aamap', 'bbmap'), (100, sentinel.aa, sentinel.bb)],
            writer.rows)


class Test_ExtractMap_process(unittest.TestCase):

    def test_output_header(self):
        reader = ReaderWriter()
        reader.rows = [('aa', 'bb', 'cc', 'dd')]
        writer = ReaderWriter()

        m.ExtractMap('b=bb,c=cc', 'a=id').process(reader, writer)

        self.assertEqual(
            [('aa', 'dd', 'id')],
            writer.rows)

    def test_output_values(self):
        reader = ReaderWriter()
        reader.rows = [
            ('aa', 'bb', 'cc', 'dd'),
            (sentinel.aa1, sentinel.bb1, sentinel.cc1, sentinel.dd1),
            (sentinel.aa2, sentinel.bb2, sentinel.cc2, sentinel.dd2),
            (sentinel.aa3, sentinel.bb1, sentinel.cc1, sentinel.dd3), ]
        writer = ReaderWriter()

        m.ExtractMap('b=bb,c=cc', 'a=id').process(reader, writer)

        self.assertEqual(
            sorted([
                (sentinel.aa1, sentinel.dd1, 0),
                (sentinel.aa2, sentinel.dd2, 1),
                (sentinel.aa3, sentinel.dd3, 0), ]),
            sorted(writer.rows[1:]))

    def test_keep_fields(self):
        reader = ReaderWriter()
        reader.rows = [
            ('aa', 'bb', 'cc', 'dd'),
            (sentinel.aa1, sentinel.bb1, sentinel.cc1, sentinel.dd1),
            (sentinel.aa2, sentinel.bb2, sentinel.cc2, sentinel.dd2),
            (sentinel.aa3, sentinel.bb1, sentinel.cc1, sentinel.dd3), ]
        writer = ReaderWriter()

        em = m.ExtractMap('b=bb,c=cc', 'a=id', keep_fields=True)
        em.process(reader, writer)

        self.assertEqual(
            [
                ('aa', 'bb', 'cc', 'dd', 'id'),
                (sentinel.aa1, sentinel.bb1, sentinel.cc1, sentinel.dd1, 0),
                (sentinel.aa2, sentinel.bb2, sentinel.cc2, sentinel.dd2, 1),
                (sentinel.aa3, sentinel.bb1, sentinel.cc1, sentinel.dd3, 0), ],
            writer.rows)

    def test_map_header(self):
        reader = ReaderWriter()
        reader.rows = [('aa', 'bb', 'cc', 'dd'), ]
        writer = ReaderWriter()

        extract_map = m.ExtractMap('b=bb,c=cc', 'a=id')
        extract_map.process(reader, writer)

        map_writer = ReaderWriter()
        extract_map.map.write(map_writer)

        # all fields renamed, id comes first - for sorting?
        self.assertEqual(
            [('a', 'b', 'c')],
            map_writer.rows)

    def test_map_content(self):
        reader = ReaderWriter()
        reader.rows = [
            ('aa', 'bb', 'cc', 'dd'),
            (sentinel.aa1, sentinel.bb1, sentinel.cc1, sentinel.dd1),
            (sentinel.aa2, sentinel.bb2, sentinel.cc2, sentinel.dd2),
            (sentinel.aa3, sentinel.bb1, sentinel.cc1, sentinel.dd3), ]
        writer = ReaderWriter()

        extract_map = m.ExtractMap('b=bb,c=cc', 'a=id')
        extract_map.process(reader, writer)

        map_writer = ReaderWriter()
        extract_map.map.write(map_writer)

        # all fields renamed, id comes first - for sorting?
        self.assertEqual(
            sorted([
                (0, sentinel.bb1, sentinel.cc1),
                (1, sentinel.bb2, sentinel.cc2), ]),
            sorted(map_writer.rows[1:]))


class Test_extract_map(unittest.TestCase):

    @within_temp_dir
    def test_existing_map_used(self):
        with open('map.csv', 'w') as f:
            f.write('id,a\n5,a')
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), ('a', 'b'), ('c', 'd')]
        writer = ReaderWriter()

        m.extract_map(reader, writer, 'map.csv', 'a', 'id')

        self.assertEqual(
            sorted([('b', 5), ('d', 6)]),
            sorted(writer.rows[1:]))

    @within_temp_dir
    def test_changed_map_is_written_out(self):
        with open('map.csv', 'w') as f:
            f.write('id,a\n5,a')
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), ('a', 'b'), ('c', 'd')]
        writer = ReaderWriter()

        m.extract_map(reader, writer, 'map.csv', 'a', 'id')

        with open('map.csv') as f:
            items = tuple(csv.reader(f))

        self.assertEqual(
            sorted((('id', 'a'), ('5', 'a'), ('6', 'c'))),
            map(tuple, sorted(items)))

    @within_temp_dir
    def test_keep_fields(self):
        with open('map.csv', 'w') as f:
            f.write('id,a\n5,a')
        reader = ReaderWriter()
        reader.rows = [('a', 'b'), ('a', 'b'), ('c', 'd')]
        writer = ReaderWriter()

        m.extract_map(reader, writer, 'map.csv', 'a', 'id', keep_fields=True)

        self.assertEqual(
            [('a', 'b', 'id'), ('a', 'b', 5), ('c', 'd', 6)],
            writer.rows)


class Test_parse_args(unittest.TestCase):

    def test_mandatory_parameters(self):
        args = m.parse_args('map_file map_fields ref_field'.split())
        self.assertEqual('map_file', args.map_file)
        self.assertEqual('map_fields', args.map_fields)
        self.assertEqual('ref_field', args.ref_field)

    def test_keep_fields_defaults_to_false(self):
        args = m.parse_args('map_file map_fields ref_field'.split())
        self.assertFalse(args.keep_fields)

    def test_keep_fields(self):
        input_args = '--keep-fields map_file map_fields ref_field'.split()
        args = m.parse_args(input_args)
        self.assertTrue(args.keep_fields)
