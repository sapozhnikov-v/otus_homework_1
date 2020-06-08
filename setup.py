# -*- coding: utf-8 -*-
import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='searcher-2020',
    version='0.1',
    packages=['searcher'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Genereates random number',
    long_description=README,
    url='https://github.com/sapozhnikov-v/otus_homework_1',
    author='sapozhnikov-v',
    author_email='vitaliy.sapozhnikov@gmail.com',
    keywords=['search'],
    classifiers=[],
    install_requires=[
        'ujson>=3.0.0',
        'selenium'
    ],
    entry_points={
        'console_scripts': [
            'searcher = searcher.searcher:main',
        ]
    },
)