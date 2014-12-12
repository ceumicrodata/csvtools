# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import scripttest
from unittest import TestCase

from . import csv_reader

from .. import first_rows_by as m


TEST_CSV = '''\
id,g1,g2,v
1,1,1,g1g2
2,1,2,g2
3,2,2,g1
4,2,1,g2
5,2,1,id
'''

FIRSTS_id_CSV = '''\
id,g1,g2,v,group_size
1,1,1,g1g2,1
2,1,2,g2,1
3,2,2,g1,1
4,2,1,g2,1
5,2,1,id,1
'''

FIRSTS_g1_CSV = '''\
id,g1,g2,v,group_size
1,1,1,g1g2,2
3,2,2,g1,3
'''

FIRSTS_g1_gsf_CSV = '''\
id,g1,g2,v,gsf
1,1,1,g1g2,2
3,2,2,g1,3
'''

FIRSTS_g2_CSV = '''\
id,g1,g2,v,group_size
1,1,1,g1g2,1
2,1,2,g2,2
4,2,1,g2,2
'''

FIRSTS_g1_g2_CSV = '''\
id,g1,g2,v,group_size
1,1,1,g1g2,1
2,1,2,g2,1
3,2,2,g1,1
4,2,1,g2,2
'''


class Test_firsts(TestCase):

    def assert_firsts(self, expected, key_fields, group_size_field='group_size'):
        output = [
            map(str, row)
            for row in m.first_rows_by(
                rows=csv_reader(TEST_CSV),
                group_fields=key_fields.split(),
                group_size_field=group_size_field
            )
        ]

        self.assertEqual(
            list(csv_reader(expected)),
            output
        )

    def test_firsts_identity(self):
        self.assert_firsts(FIRSTS_id_CSV, 'id')

    def test_firsts_composite_key(self):
        self.assert_firsts(FIRSTS_g1_g2_CSV, 'g1 g2')

    def test_firsts_non_id_key(self):
        self.assert_firsts(FIRSTS_g1_CSV, 'g1')
        self.assert_firsts(FIRSTS_g2_CSV, 'g2')

    def test_group_size(self):
        self.assert_firsts(FIRSTS_g1_gsf_CSV, 'g1', group_size_field='gsf')


class Test_script(TestCase):

    def test(self):
        env = scripttest.TestFileEnvironment('scripttest')
        self.addCleanup(env.clear)
        r = env.run(
            'csv_first_rows_by', 'g2', 'g1',
            stdin=TEST_CSV.encode('utf-8'),
        )
        self.assertEqual(
            list(csv_reader(FIRSTS_g1_g2_CSV)),
            list(csv_reader(r.stdout))
        )
