#!/usr/bin/env python
# coding: utf8

from setuptools import setup

VERSION = '0.5.0'
# VERSION_SUFFIX = '-dev'
VERSION_SUFFIX = ''

setup(
    name='csvtools',
    version='{version}{version_suffix}'.format(
        version=VERSION,
        version_suffix=VERSION_SUFFIX,
    ),

    description=u'Tools for transforming .csv files',
    author=u'CEU MicroData',
    url='https://github.com/ceumicrodata/csvtools',

    packages=['csvtools'],

    tests_require=[
        'temp_dir',
        'mock',
        'nose',
    ],

    test_suite='nose.collector',

    provides=['csvtools ({version})'.format(version=VERSION)],

    entry_points={
        'console_scripts': [
            'csv_select = csvtools.select:main',
            'csv_split = csvtools.split:main',
            'csv_cat = csvtools.concatenate:main',
            'csv_zip = csvtools.zip:main',
            'csv_unzip = csvtools.unzip:main',
            'csv_rmfields = csvtools.rmfields:main',
            'csv_extract_map = csvtools.extract_map:main',
            'csv_to_postgres = csvtools.to_postgres:main',
            'csv_to_tsv = csvtools.csv2tsv:main',
            'tsv_to_csv = csvtools.tsv2csv:main',

            # aliases
            'csv2postgres = csvtools.to_postgres:main',
            'csv2tsv = csvtools.csv2tsv:main',
            'tsv2csv = csvtools.tsv2csv:main',
        ],
    }
)
