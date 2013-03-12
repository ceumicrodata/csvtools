class Field(object):

    def bind(self, header_row):
        pass

    def value_extractor(self, row):
        pass


def None_extractor(row):
    return None


def make_index_extractor(index):
    def extractor(row):
        return row[index]
    return extractor


class NamedField(Field):

    index = None

    def __init__(self, name):
        self.name = name

    def bind(self, header_row):
        self.index = header_row.index(self.name)

    @property
    def bound(self):
        return self.index is not None

    @property
    def value_extractor(self):
        if self.index is None:
            return None_extractor

        return make_index_extractor(self.index)
