# coding: utf-8

import argparse
import sys
import csv


def pad_csv(items):
    items = iter(items)

    input_header = next(items)
    csv_width = len(input_header)
    yield input_header
    for item in items:
        current_width = len(item)
        yield item + [''] * (csv_width - current_width)


def main():
    parser = argparse.ArgumentParser(
        description='''
        Pad csv file - adding missing empty fields to the right of each row,
        based on number of fields in the header.
        '''
    )

    input_stream = csv.reader(sys.stdin)
    output_stream = csv.writer(sys.stdout)

    output_stream.writerows(
        pad_csv(input_stream)
    )

if __name__ == "__main__":
    main()
