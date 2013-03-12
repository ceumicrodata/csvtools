import sys
import csv
from csvtools.transformer import SimpleTransformer
from csvtools.field_maps import FieldMaps


def select(input_file, output_file, transform_spec):
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    field_maps = FieldMaps()
    field_maps.parse_from(transform_spec)
    SimpleTransformer(field_maps).process(reader, writer)


def main():
    transform_spec = sys.argv[1]
    select(sys.stdin, sys.stdout, transform_spec)


if __name__ == '__main__':
    main()
