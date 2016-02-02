#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

version = open('VERSION').read()

setup(
    name='vcontext',
    version=version,
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
    include_package_data=True,
)
