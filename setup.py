#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-aloe',
    version='0.1.0',
    author='Dennis Miasoutov',
    author_email='dmiasoutov@wayfair.com',
    maintainer='Dennis Miasoutov',
    maintainer_email='dmiasoutov@wayfair.com',
    license='Apache Software License 2.0',
    url='https://github.com/wayfair/pytest-aloe',
    description='Pytest plugin to support BDD using ghirkin files',
    long_description=read('README.rst'),
    packages=['aloe', 'pytest_aloe'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.5.0', 'gherkin-official>=4.1.3', 'repoze.lru', 'future>=0.17.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'pytest-aloe = pytest_aloe.plugin',
        ],
    },
)
