import sys
import csv
from csvtools.field import RecordTransformer


def process(reader, writer, transformer):
    reader_iter = iter(reader)
    header = reader_iter.next()
    transformer.bind(header)
    transform = transformer.transform

    writer.writerow(transformer.output_header)
    for record in reader_iter:
        writer.writerow(transform(record))


def select(input_file, output_file, transform_spec):
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    transformer = RecordTransformer(transform_spec)
    process(reader, writer, transformer)


def main():
    transform_spec = sys.argv[1]
    select(sys.stdin, sys.stdout, transform_spec)


if __name__ == '__main__':
    main()