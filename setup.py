#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='descriptor-contest',
    version=0.1,
    description='Do a quick personality test for an organisation or group',
    author='Vera Kreuter, Martin Häcker',
    author_email='vera.kreuter@gmail.com, mhaecker@mac.com',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy'
    ],
    license='AGPL',
    url='https://github.com/verkre/descriptor-contest',
)