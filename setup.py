#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='csvtools',
    version='0.1.0-dev',
    description=u'Tools for transforming .csv files',
    author=u'CEU MicroData',
    url='https://github.com/ceumicrodata/csvtools',
    packages=['csvtools'],
    install_requires=['temp_dir'],
    provides=['csvtools (0.1.0)'],
    entry_points={
        'console_scripts': [
            'csv_select = csvtools.select:main',
            'csv_split = csvtools.split:main',
            'csv_zip = csvtools.zip:main',
            'csv_unzip = csvtools.unzip:main',
            'csv_rmfields = csvtools.rmfields:main',
            'csv_extract_map = csvtools.extract_map:main',
            'csv_to_postgres = csvtools.to_postgres:main',
        ],
    }
    )
