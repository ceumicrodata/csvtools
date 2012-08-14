import sys
from csvtools.field import RecordTransformer


class Map(object):

    modified = False

    def __init__(self, map_file_name, map_fields, ref_field_name):
        self.transformer = RecordTransformer(map_fields)
        self.ref_field_name = ref_field_name
        # self.values = dict()
        self.max_ref = -1

    def open_file(self, mode='r'):
        pass

    def read(self):
        # throws an exception if already bound
        # throws an exception if fields in map read in does not match with the fields in binding
        # throws an exception if map_fields is not unique
        # throws an exception if ref_field_name is not unique
        pass

    def write(self):
        pass

    def translate(self, input_tuple):
        # calls add if new value, returns ref
        # similar to dict.setdefault
        pass

    def bind(self, header):
        self.transformer.bind(header)

    def add(self, input_tuple):
        self.modified = True
        self.max_ref += 1
        # TODO: everything else

    @property
    def field_names(self):
        return self.transformer.output_header + tuple([self.ref_field_name])

    @property
    def next_ref(self):
        return self.max_ref


def process(input_file, output_file, map_file, map_fields, map_ref_field_name):
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
    map_file, map_fields, map_ref_field_name = sys.argv[1:]

    process(sys.stdin, sys.stdout, map_file, map_fields, map_ref_field_name)



if __name__ == '__main__':
    main()
