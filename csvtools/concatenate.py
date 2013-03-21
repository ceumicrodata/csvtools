import csv
import sys
import itertools


class InconsistentHeadersError(Exception):
    pass


def input_csvs(streams):
    return tuple(csv.reader(stream) for stream in streams)


def read_header(csv):
    return next(csv)


def same_values(items):
    return all(item == items[0] for item in items)


def concatenate(input_streams, output_stream):
    csvs = input_csvs(input_streams)
    headers = tuple(read_header(csv) for csv in csvs)

    if not same_values(headers):
        raise InconsistentHeadersError()
    else:
        output = csv.writer(output_stream)
        output.writerow(headers[0])
        output.writerows(itertools.chain.from_iterable(csvs))


if __name__ == "__main__":
    input_streams = (
        tuple(
            open(filename, "r")
            for filename in sys.argv[1:]))

    if input_streams:
        concatenate(input_streams, sys.stdout)
