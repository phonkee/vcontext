#!/usr/bin/env python

import os
import re

from setuptools import setup

long_description = open('README.rst').read()


def get_version():
    version_file = os.path.join('vcontext', '__init__.py')
    initfile_lines = open(version_file, 'rt').readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(version_regex, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (version_file,))


setup(
    name='vcontext',
    version=get_version(),
    url='https://github.com/phonkee/vcontext',
    description='Context data structure',
    long_description=long_description,

    # author information
    author='Peter Vrba',
    author_email='phonkee@phonkee.eu',

    packages=['vcontext'],

    # requirements
    install_requires=[
        'six',
    ],
    test_suite="vcontext.tests",
    include_package_data=True,
)
