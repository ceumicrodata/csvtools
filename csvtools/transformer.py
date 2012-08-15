class Transformer(object):

    '''
    .output_field_names : tuple of field names, output header
    .transform : creates a new tuple based on the input_row and the specs
    '''

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


class SimpleTransformer(Transformer):

    field_maps = None
    extractors = None

    def __init__(self, field_maps):
        self.field_maps = field_maps
        self.fields = dict(
            (field_map.input_field_name, field_map.extractor_field)
            for field_map in self.field_maps)

    def bind(self, header_row):
        for field in self.fields.itervalues():
            field.bind(header_row)

        self.extractors = tuple(
            self.fields[name].value_extractor
            for name in self.input_field_names)

    def transform(self, input_row):
        return tuple(e(input_row) for e in self.extractors)

    @property
    def output_field_names(self):
        return self.field_maps.output_field_names

    # helpers
    @property
    def input_field_names(self):
        return self.field_maps.input_field_names
