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

import sys
from csvtools.transformer import Transformer, SimpleTransformer
from csvtools.field_maps import FieldMaps
from csvtools.field import Field


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

        input_field_names = tuple([self.ref_field_name]) + self.transformer.output_field_names
        field_maps = FieldMaps()
        for input_field_name in input_field_names:
            field_maps.add(input_field_name, input_field_name)
        map_transformer = SimpleTransformer(field_maps)
        map_transformer.bind(header)

        count = 0
        values = dict()
        for row in rows:
            transformed_row = map_transformer.transform(row)
            ref = transformed_row[0]
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
        header = tuple([self.ref_field_name]) + self.transformer.output_field_names
        writer.writerow(header)

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
        return self.transformer.output_field_names + tuple([self.ref_field_name])


class RefField(Field):

    def __init__(self, map):
        self.map = map

    def bind(self, header):
        self.map.bind(header)

    def value_extractor(self, input_row):
        return self.map.translate(input_row)


class ExtractMap(Transformer):

    def __init__(self, map_fields_spec, ref_field_spec):
        field_maps = FieldMaps()
        field_maps.parse_from(map_fields_spec)
        self.fields_to_remove = field_maps.input_field_names

        # TODO: this is ugly, beautify
        ref_field_map = FieldMaps().parse_field_map_string(ref_field_spec)

        self.map = Map(field_maps, ref_field_map.output_field_name)
        self.ref_field_name = ref_field_map.input_field_name
        self.transformer = None

    def bind(self, header):
        # TODO: DRY, this part is copied from RemoveFields, except for adding the ref field (extract common stuff into ProxyTransformer?)
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

    @property
    def output_field_names(self):
        return self.transformer.output_field_names

    @property
    def transform(self):
        return self.transformer.transform


def main():
    map_file, map_fields, map_ref_field = sys.argv[1:]

    # process(sys.stdin, sys.stdout, map_file, map_fields, map_ref_field_name)



if __name__ == '__main__':
    main()
