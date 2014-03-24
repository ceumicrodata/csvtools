'''
Replace a set of fields with a reference to map.csv file rows

Usage:
extract_map map.csv map_fields_spec ref_field_spec

Technically:
- read original map from map.csv if that file exists
- remove input side of map_fields_spec from input
- append input side of ref_field_spec to input
- write extended map to map.csv if changed

'''

import os.path
import sys
from csvtools.transformer import Transformer, SimpleTransformer
from csvtools.field_maps import FieldMaps
from csvtools.field import Field
import csv
import argparse


class MissingFieldError(Exception):
    pass


class DuplicateValuesError(Exception):
    pass


class DuplicateRefsError(Exception):
    pass


class Map(object):

    changed = False

    def __init__(self, map_field_maps, ref_field_name):
        self.transformer = SimpleTransformer(map_field_maps)
        self.ref_field_name = ref_field_name
        self.values = dict()
        self.next_ref = 0

    def read(self, reader):
        rows = iter(reader)

        header = rows.next()
        if self.ref_field_name not in header:
            raise MissingFieldError(self.ref_field_name)
        for field_name in self.transformer.output_field_names:
            if field_name not in header:
                raise MissingFieldError(self.ref_field_name)

        # first field is ID
        field_maps = FieldMaps()
        for input_field_name in self.field_names:
            field_maps.add(input_field_name, input_field_name)
        map_transformer = SimpleTransformer(field_maps)
        map_transformer.bind(header)

        count = 0
        values = dict()
        for row in rows:
            transformed_row = map_transformer.transform(row)
            ref = int(transformed_row[0])
            value = transformed_row[1:]
            values[value] = ref

            count += 1

        if count != len(values):
            raise DuplicateValuesError()
        if count != len(set(values.values())):
            raise DuplicateRefsError()

        self.values = values
        self.next_ref = max(values.values()) + 1

    def write(self, writer):
        writer.writerow(self.field_names)

        for (value, ref) in self.values.iteritems():
            writer.writerow(tuple([ref]) + tuple(value))

    def translate(self, input_row):
        key = self.transformer.transform(input_row)
        ref = self.values.setdefault(key, self.next_ref)
        if ref == self.next_ref:
            self.next_ref += 1
            self.changed = True
        return ref

    def bind(self, header):
        self.transformer.bind(header)

    @property
    def field_names(self):
        return (
            tuple([self.ref_field_name])
            + self.transformer.output_field_names)


class RefField(Field):

    def __init__(self, map):
        self.map = map

    def bind(self, header):
        self.map.bind(header)

    def value_extractor(self, input_row):
        return self.map.translate(input_row)


class ExtractMap(Transformer):

    def __init__(self, map_fields_spec, ref_field_spec, keep_fields=False):
        field_maps = FieldMaps()
        field_maps.parse_from(map_fields_spec)
        self.fields_to_remove = (
            set() if keep_fields else field_maps.input_field_names)

        # TODO: this is ugly, beautify
        ref_field_map = FieldMaps().parse_field_map_string(ref_field_spec)

        self.map = Map(field_maps, ref_field_map.output_field_name)
        self.ref_field_name = ref_field_map.input_field_name
        self.transformer = None

    def bind(self, header):
        # TODO: DRY: copied from RemoveFields
        # except for adding the ref field
        # (extract common stuff into ProxyTransformer?)
        input_fields_to_keep = tuple(
            field_name
            for field_name in header
            if field_name not in self.fields_to_remove)

        field_maps = FieldMaps()
        for field_name in input_fields_to_keep:
            field_maps.add(field_name, field_name)
        field_maps.add(
            input_field_name=None,
            output_field_name=self.ref_field_name,
            extractor_field=RefField(self.map))

        self.transformer = SimpleTransformer(field_maps)
        self.transformer.bind(header)

    def read_map(self, reader):
        self.map.read(reader)

    def write_map(self, writer):
        self.map.write(writer)

    @property
    def map_changed(self):
        return self.map.changed

    @property
    def output_field_names(self):
        return self.transformer.output_field_names

    @property
    def transform(self):
        return self.transformer.transform


def extract_map(
        reader, writer,
        map_file, map_fields_spec, ref_field_spec, keep_fields=False):
    transformer = ExtractMap(map_fields_spec, ref_field_spec, keep_fields)

    if os.path.exists(map_file):
        with open(map_file) as f:
            transformer.read_map(csv.reader(f))

    transformer.process(reader, writer)

    if transformer.map_changed:
        with open(map_file, 'w') as f:
            transformer.write_map(csv.writer(f))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--keep-fields',
        dest='keep_fields',
        default=False,
        action='store_true',
        help='keep extracted fields in output (default: %(default)s)')
    parser.add_argument(
        'map_file',
        help=(
            'file for the extracted values,'
            ' if exists it is read and extended'))
    parser.add_argument(
        'map_fields',
        help=(
            'fields to extract and under what names'
            ' (map_field=input_field,field_with_same_name)'))
    parser.add_argument(
        'ref_field',
        help=(
            'field name for the new reference field,'
            ' by which values can be joined back'))
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    extract_map(
        csv.reader(sys.stdin),
        csv.writer(sys.stdout),
        args.map_file,
        args.map_fields,
        args.ref_field,
        keep_fields=args.keep_fields)


if __name__ == '__main__':
    main()
