# Py3 compatibility
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import sys
if sys.version_info.major == 2:
    # csv module does not play well with unicode:
    # it writes the file in binary mode
    from StringIO import StringIO
else:
    from io import StringIO
import textwrap
import csv
import csvtools.concatenate as m


def get_stream(text):
    if isinstance(text, bytes):
        text = text.decode('utf8')
    return StringIO(textwrap.dedent(text))


def get_values(text):
    return list(csv.reader(get_stream(text)))


assert [['a', 'b'], ['1', '2']] == get_values(
    b'''\
    a,b
    1,2
    '''
)

LOREM_12 = b'''\
    id,lorem,ipsum
    1,dolor,sit
    2,amet,consectetuer
'''

LOREM_3 = b'''\
    id,lorem,ipsum
    3,adipisicing,velit
'''

LOREM_123 = b'''\
    id,lorem,ipsum
    1,dolor,sit
    2,amet,consectetuer
    3,adipisicing,velit
'''

ID_45 = b'''\
    id
    4
    5
'''


class Test_CsvAppender(unittest.TestCase):

    def setUp(self):
        self.output_stream = StringIO()
        self.appender = m.CsvAppender(self.output_stream)

    def get_appended(self):
        return get_values(self.output_stream.getvalue())

    def test_one_file(self):
        input_stream = get_stream(LOREM_12)
        self.appender.append(input_stream)
        self.assertEqual(
            get_values(LOREM_12),
            self.get_appended()
        )

    def test_files_with_same_header_are_concatenated(self):
        lorem_12 = get_stream(LOREM_12)
        lorem_3 = get_stream(LOREM_3)
        self.appender.append(lorem_12)
        self.appender.append(lorem_3)
        self.assertEqual(
            get_values(LOREM_123),
            self.get_appended()
        )

    def test_files_with_different_headers_is_error(self):
        lorem_12 = get_stream(LOREM_12)
        id_45 = get_stream(ID_45)
        self.appender.append(lorem_12)

        with self.assertRaises(m.InconsistentHeadersError):
            self.appender.append(id_45)

        self.assertEqual(
            get_values(LOREM_12),
            self.get_appended()
        )

    def test_large_field_in_csv(self):
        csv_stream = StringIO()
        writer = csv.writer(csv_stream)
        writer.writerow(['a'])
        big_field_value = ('a\n' * 1024) * 1024
        writer.writerow([big_field_value])
        csv_stream.seek(0)

        # expect no errors!
        self.appender.append(csv_stream)

    def test_missing_newline_at_EOF_in_first_file(self):
        lorem_12 = get_stream(LOREM_12.rstrip())
        lorem_3 = get_stream(LOREM_3)
        self.appender.append(lorem_12)
        self.appender.append(lorem_3)
        self.assertEqual(
            get_values(LOREM_123),
            self.get_appended()
        )
