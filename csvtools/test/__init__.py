class ReaderWriter(object):

    '''
    Drop in replacement for both csv.reader and csv.writer
    '''

    rows = None

    def __init__(self):
        self.rows = []

    def writerow(self, row):
        self.rows.append(row)

    def __iter__(self):
        return iter(self.rows)
