# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from .. import snapshot as m

from unittest import TestCase

from . import csv_reader
from . import hide_stderr

from datetime import date

import scripttest


class Test_arguments(TestCase):

    def parse_args(self, cmdline):
        return m.parse_args(cmdline.split())

    def test_interval_fields(self):
        args = self.parse_args('hattol hatig 2010')
        self.assertEqual('hattol', args.from_field)
        self.assertEqual('hatig', args.to_field)

    def test_normal_date(self):
        args = self.parse_args('f t 2011-01-12')
        self.assertEqual(2011, args.snapshot_date.year)
        self.assertEqual(1, args.snapshot_date.month)
        self.assertEqual(12, args.snapshot_date.day)

    def test_not_a_date(self):
        with self.assertRaises(SystemExit), hide_stderr():
            self.parse_args('f t x2011-01-12')

    def test_bad_date(self):
        with self.assertRaises(SystemExit), hide_stderr():
            self.parse_args('f t 2014-2-29')

    def test_0_month(self):
        with self.assertRaises(SystemExit), hide_stderr():
            self.parse_args('f t 2014-00-01')


TEST_CSV = '''\
from,to,value
,2000-03-14,a
2000-03-14,2002-04-25,b
2002-04-25,,c
2000-03-14,2002-04-25,BB
'''

SNAPSHOT_1999 = '''\
from,to,value
,2000-03-14,a
'''

SNAPSHOT_2001 = '''\
from,to,value
2000-03-14,2002-04-25,b
2000-03-14,2002-04-25,BB
'''

SNAPSHOT_2003 = '''\
from,to,value
2002-04-25,,c
'''


class Test_snapshot(TestCase):

    def assert_snapshot(self, expected, date):
        actual = m.snapshot(
            csv_reader(TEST_CSV),
            from_field='from', to_field='to',
            snapshot_date=date
        )
        self.assertEqual(
            list(csv_reader(expected)),
            list(actual)
        )

    def test_no_start_date_matches_dates_before_end_date(self):
        self.assert_snapshot(SNAPSHOT_1999, date(1999, 1, 1))

    def test_no_end_date_matches_dates_after_start_date(self):
        self.assert_snapshot(SNAPSHOT_2003, date(2003, 1, 1))

    def test_between_start_and_end_date(self):
        self.assert_snapshot(SNAPSHOT_2001, date(2001, 1, 1))


class Test_script(TestCase):

    def test(self):
        env = scripttest.TestFileEnvironment('scripttest')
        self.addCleanup(env.clear)
        r = env.run(
            'csv_snapshot', 'from', 'to', '2001-01-01',
            stdin=TEST_CSV.encode('utf-8'),
        )
        self.assertEqual(
            list(csv_reader(SNAPSHOT_2001)),
            list(csv_reader(r.stdout))
        )
