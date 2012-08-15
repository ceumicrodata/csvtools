'''
Remove the given fields from its input

Usage:

rmfields.py field_name [field_name [...]]
'''

import sys
import csv
from csvtools.transformer import Transformer, SimpleTransformer


class RemoveFields(Transformer):

    def __init__(self, fields_to_remove):
        self.fields_to_remove = fields_to_remove
        self.transformer = None

    def bind(self, header):
        self.output_field_names = tuple(
            field_name
            for field_name in header
            if field_name not in self.fields_to_remove)
        self.transformer = SimpleTransformer(','.join(self.output_field_names))
        self.transformer.bind(header)

    @property
    def transform(self):
        return self.transformer.transform


def main():
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    fields = sys.argv[1:]
    RemoveFields(fields).process(reader, writer)


if __name__ == '__main__':
    main()