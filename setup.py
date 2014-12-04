#!/usr/bin/env python
# coding: utf8

from setuptools import setup

VERSION = '0.5.2'
VERSION_SUFFIX = '-dev'
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

    provides=['csvtools ({version})'.format(version=VERSION)],

    install_requires=[
        'aniso8601>=0.90',
        'unicodecsv>=0.9.4',
    ],

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
            'csv_snapshot = csvtools.snapshot:main',

            # aliases _ -> -
            'csv-select = csvtools.select:main',
            'csv-split = csvtools.split:main',
            'csv-cat = csvtools.concatenate:main',
            'csv-zip = csvtools.zip:main',
            'csv-unzip = csvtools.unzip:main',
            'csv-rmfields = csvtools.rmfields:main',
            'csv-extract-map = csvtools.extract_map:main',
            'csv-to-postgres = csvtools.to_postgres:main',
            'csv-to-tsv = csvtools.csv2tsv:main',
            'tsv-to-csv = csvtools.tsv2csv:main',
            'csv-snapshot = csvtools.snapshot:main',

            # aliases
            'csv2postgres = csvtools.to_postgres:main',
            'csv2tsv = csvtools.csv2tsv:main',
            'tsv2csv = csvtools.tsv2csv:main',
        ],
    }
)
