#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

try:
    with open('README.md') as readme_file:
        long_description = readme_file.read()
except:
    long_description = ""

setup(
    name='vcontext',
    version='0.7',
    url='https://github.com/phonkee/vcontext',
    description='Context data structure',
    long_description=long_description,

    # author information
    author='Peter Vrba',
    author_email='phonkee@phonkee.eu',

    packages=['vcontext'],

    # requirements
    install_requires=[
    ],
    test_suite="vcontext.tests",
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md'],
    }
)
