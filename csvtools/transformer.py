from csvtools.field import NamedField
from csvtools.field_maps import FieldMaps


class Transformer(object):

    output_field_names = None

    def process(self, reader, writer):
        reader_iter = iter(reader)
        header = reader_iter.next()
        self.bind(header)
        transform = self.transform

        writer.writerow(self.output_field_names)
        for record in reader_iter:
            writer.writerow(transform(record))

    def bind(self, header_row):
        pass

    def transform(self, row):
        pass


class RecordTransformer(Transformer):

    '''
    .output_field_names : tuple of field names in output
    .transform : creates a new tuple based on the input_row and the specs
    '''

    field_maps = None
    extractors = None

    def __init__(self, field_maps_string):
        self.field_maps = FieldMaps()
        self.field_maps.parse_from(field_maps_string)
        self.input_fields = dict(
            (input_field_name, NamedField(input_field_name))
            for input_field_name in self.input_field_names)

    def bind(self, header_row):
        for field in self.input_fields.itervalues():
            field.bind(header_row)

        self.extractors = tuple(
            self.input_fields[name].value_extractor
            for name in self.input_field_names)

    def transform(self, input_row):
        return tuple(e(input_row) for e in self.extractors)

    @property
    def output_field_names(self):
        return tuple(out for (out, _) in self.field_maps)

    # helpers
    @property
    def input_field_names(self):
        return tuple(
            input_field_name
            for (_, input_field_name) in self.field_maps)
