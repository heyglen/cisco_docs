#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

REQUIRED = [
    'colorlog',
    'appdirs',
    'pyyaml',
    'Click>=6.0',
]

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='cisco_doc_parser',
    version='0.1.0',
    description="Cisco Documentation Parser",
    long_description=readme + '\n\n' + history,
    author="Glen Harmon",
    author_email='glencharmon@gmail.com',
    url='https://github.com/heyglen/cisco_doc_parser',
    packages=find_packages(exclude=['contrib', u'docs', u'tests']),
    package_dir={'cisco_doc_parser':
                 'cisco_doc_parser'},
    entry_points={
        'console_scripts': [
            'cdocs=cisco_doc_parser.cli:commands'
        ]
    },
    include_package_data=True,
    install_requires=REQUIRED,
    license="MIT license",
    zip_safe=False,
    keywords='cisco_doc_parser',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
