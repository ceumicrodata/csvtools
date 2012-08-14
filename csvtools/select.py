import sys
import csv
from csvtools.field import RecordTransformer


def process(input_file, output_file, transform_spec):
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    transformer = RecordTransformer(transform_spec)

    header = reader.next()
    transformer.bind(header)
    transform = transformer.transform

    writer.writerow(transformer.output_header)
    for record in reader:
        writer.writerow(transform(record))


def main():
    transform_spec = sys.argv[1]

    process(sys.stdin, sys.stdout, transform_spec)


if __name__ == '__main__':
    main()