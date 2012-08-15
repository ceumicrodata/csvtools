from csvtools.field import NamedField


class Transformer(object):

    def process(self, reader, writer):
        pass

    def transform(self, input_row):
        pass


class RecordTransformer(Transformer):

    '''
    .output_header : tuple of field names in output
    .transform : creates a new tuple based on the input_tuple and the specs
    '''

    parsed_spec = None
    extractors = None

    def __init__(self, transformer_spec_string):
        self.parsed_spec = self.parse_transformer_spec_string(transformer_spec_string)
        self.field_map = dict(
            (input_field_name, NamedField(input_field_name))
            for _out, input_field_name in self.parsed_spec)

    def process(self, reader, writer):
        reader_iter = iter(reader)
        header = reader_iter.next()
        self.bind(header)
        transform = self.transform

        writer.writerow(self.output_header)
        for record in reader_iter:
            writer.writerow(transform(record))

    def transform(self, input_tuple):
        return tuple(e(input_tuple) for e in self.extractors)

    def bind(self, header_tuple):
        for field in self.field_map.itervalues():
            field.initialize_from(header_tuple)

        self.extractors = tuple(
            self.field_map[name].value_extractor
            for name in self.input_field_names)

    @property
    def output_header(self):
        return tuple(out for (out, _) in self.parsed_spec)

    # helpers
    @property
    def input_field_names(self):
        return tuple(
            input_field_name
            for (_, input_field_name) in self.parsed_spec)

    def parse_field_spec_string(self, field_spec):
        '''
        Parses field specs format: out[=in]
        '''
        out, eq, in_ = field_spec.partition('=')
        in_ = in_ or out
        return (out, in_)

    def parse_transformer_spec_string(self, transformer_spec):
        '''
        Parses list of field specs, where field specs are separated by comma (,)
        '''
        return tuple(
            self.parse_field_spec_string(field_spec)
            for field_spec in transformer_spec.split(','))
