import csv
import sys


class StreamSplitter(object):

    def __init__(self, reader, prefix, chunk_size):
        self.prefix = prefix
        self.chunk_size = chunk_size
        self.file_index = 0
        self.reader = iter(reader)
        self.header = self.reader.next()
        self.output_file = None

    def close_file(self):
        self.output_file.close()
        self.output_file = None
        self.file_index += 1

    def new_file(self):
        if self.output_file is not None:
            self.close_file()

        file_name = self.prefix + (
            '{:5d}'.format(self.file_index).replace(' ', '-')
        )
        self.output_file = open(file_name, 'w')
        writer = csv.writer(self.output_file)
        writer.writerow(self.header)
        return writer

    def split(self):
        chunk_size = self.chunk_size

        writer = self.new_file()
        count = 0

        for row in self.reader:
            if count == chunk_size:
                writer = self.new_file()
                count = 0

            writer.writerow(row)
            count += 1

        self.close_file()


def split(reader, prefix, chunk_size):
    StreamSplitter(reader, prefix, chunk_size).split()


def main():
    prefix, chunk_size = sys.argv[1:]
    split(csv.reader(sys.stdin), prefix, int(chunk_size))


if __name__ == '__main__':
    main()
