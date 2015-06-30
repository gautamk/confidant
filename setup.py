#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'boto == 2.38.0',
    'Beaker==1.7.0',
    'six==1.9.0'
]

test_requirements = requirements + [
    'mock==1.0.1',
    'doublex==1.8.2'
]

setup(
    name='confidant',
    version='0.0.9',
    description="Simple configuration management",
    long_description=readme + '\n\n' + history,
    author="Gautam Kumar",
    author_email='github@gautamk.com',
    url='https://github.com/gautamk/confidant',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='confidant',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='confidant.tests',
    tests_require=test_requirements,

)
