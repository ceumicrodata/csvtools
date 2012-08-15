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
from csvtools.transformer import RecordTransformer


class MissingFieldError(Exception):
    pass

class DuplicateValuesError(Exception):
    pass

class DuplicateRefsError(Exception):
    pass


class Map(object):

    modified = False

    def __init__(self, map_fields, ref_field_name):
        self.transformer = RecordTransformer(map_fields)
        self.ref_field_name = ref_field_name
        self.values = dict()
        self.next_ref = 0

    def read(self, reader):
        rows = iter(reader)

        header = rows.next()
        if self.ref_field_name not in header:
            raise MissingFieldError(self.ref_field_name)
        for field_name in self.transformer.output_header:
            if field_name not in header:
                raise MissingFieldError(self.ref_field_name)

        input_fields = tuple([self.ref_field_name]) + self.transformer.output_header
        map_transformer = RecordTransformer(','.join(input_fields))
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
        header = tuple([self.ref_field_name]) + self.transformer.output_header
        writer.writerow(header)

        for (value, ref) in self.values.iteritems():
            writer.writerow(tuple([ref]) + tuple(value))

    def translate(self, input_row):
        key = self.transformer.transform(input_row)
        ref = self.values.setdefault(key, self.next_ref)
        if ref == self.next_ref:
            self.next_ref += 1
            self.modified = True
        return ref

    def bind(self, header):
        self.transformer.bind(header)

    @property
    def field_names(self):
        return self.transformer.output_header + tuple([self.ref_field_name])


def main():
    map_file, map_fields, map_ref_field_name = sys.argv[1:]

    # process(sys.stdin, sys.stdout, map_file, map_fields, map_ref_field_name)



if __name__ == '__main__':
    main()
