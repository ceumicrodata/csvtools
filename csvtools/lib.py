from operator import itemgetter


class Header(object):

    def __init__(self, header_row):
        self.fields_list = list(header_row)
        self.extractors_by_name = dict(
            (header_field, itemgetter(i))
            for (i, header_field) in enumerate(self.fields_list))

    def __contains__(self, name):
        return name in self.extractors_by_name

    def __iter__(self):
        '''iterator over field names'''
        return iter(self.fields_list)

    def __len__(self):
        return len(self.fields_list)

    def extractor(self, name):
        return self.extractors_by_name[name]
