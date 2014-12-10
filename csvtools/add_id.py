# coding: utf-8

import argparse
import sys
import csv


def add_id(items, id_fieldname):
    items = iter(items)

    input_header = next(items)
    assert id_fieldname not in input_header

    yield [id_fieldname] + input_header
    for id, item in enumerate(items, 1):
        yield [id] + item


def main():
    parser = argparse.ArgumentParser(
        description='''
        Add a row counter field - starting from 1
        '''
    )
    parser.add_argument('field_name')
    args = parser.parse_args()

    input_stream = csv.reader(sys.stdin)
    output_stream = csv.writer(sys.stdout)

    output_stream.writerows(
        add_id(input_stream, args.field_name)
    )

if __name__ == "__main__":
    main()
