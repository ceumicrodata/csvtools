#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(name='csvtools',
      version='0.1.0-dev',
      description=u'Tools for transforming .csv files',
      author=u'CEU MicroData',
      url='https://github.com/ceumicrodata/csvtools',
      packages=['csvtools'],
      install_requires=['temp_dir'],
      provides=['csvtools (0.1.0)']
     )
