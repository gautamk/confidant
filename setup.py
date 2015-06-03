#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "boto==2.38.0",
    "itsdangerous==0.24",
    "Jinja2==2.7.3",
    "Sphinx==1.3.1",
    "click==4.0"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='confidant',
    version='0.0.1',
    description="Simple configuration management",
    long_description=readme + '\n\n' + history,
    author="Gautam Kumar",
    author_email='github@gautamk.com',
    url='https://github.com/gautamk/confidant',
    packages=[
        'confidant',
    ],
    package_dir={'confidant':
                 'confidant'},
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points='''
        [console_scripts]
        confidant=confidant.confidant:cli
    '''
)
