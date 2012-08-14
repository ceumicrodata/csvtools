class Field(object):

    def initialize_from(self, header_tuple):
        pass

    def value_extractor(self, row_tuple):
        pass


def None_extractor(row_tuple):
    return None

def make_index_extractor(index):
    def extractor(row_tuple):
        return row_tuple[index]
    return extractor


class NamedField(Field):

    index = None

    def __init__(self, name):
        self.name = name

    def initialize_from(self, header_tuple):
        self.index = header_tuple.index(self.name)

    @property
    def bound(self):
        return self.index is not None

    @property
    def value_extractor(self):
        if self.index is None:
            return None_extractor

        return make_index_extractor(self.index)


class RecordTransformer(object):

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

    def bind(self, header_tuple):
        for field in self.field_map.itervalues():
            field.initialize_from(header_tuple)

        self.extractors = tuple(
            self.field_map[name].value_extractor
            for name in self.input_field_names)

    def transform(self, input_tuple):
        return tuple(e(input_tuple) for e in self.extractors)

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

