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
