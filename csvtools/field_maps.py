from csvtools.field import NamedField


class FieldMap(object):

    input_field_name = None
    output_field_name = None
    extractor_field = None

    def __init__(
            self, input_field_name, output_field_name, extractor_field=None):
        self.input_field_name = input_field_name
        self.output_field_name = output_field_name
        if extractor_field:
            self.extractor_field = extractor_field
        else:
            self.extractor_field = NamedField(input_field_name)


class FieldMaps(object):

    def __init__(self):
        self.field_maps = list()

    def parse_from(self, field_maps_string):
        '''
        Parses list of field maps, where field maps are separated by comma (,)
        '''
        self.field_maps = tuple(
            self.parse_field_map_string(field_spec)
            for field_spec in field_maps_string.split(','))

    def add(self, input_field_name, output_field_name, extractor_field=None):
        self.field_maps.append(
            FieldMap(input_field_name, output_field_name, extractor_field))

    def __iter__(self):
        return iter(self.field_maps)

    @property
    def input_field_names(self):
        return tuple(f.input_field_name for f in self.field_maps)

    @property
    def output_field_names(self):
        return tuple(f.output_field_name for f in self.field_maps)

    def parse_field_map_string(self, field_spec):
        '''
        Parses field specs format: out[=in]
        '''
        output_field_name, eq, input_field_name = field_spec.partition('=')
        input_field_name = input_field_name or output_field_name
        return FieldMap(input_field_name, output_field_name)
