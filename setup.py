#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""
from setuptools import find_packages, setup

with open('README.md') as f:
    long_desc = f.read()
    desc = ''

with open('requirements.txt') as r:
    requirements = r.readlines()


setup(
    name='django-elastic',
    version='0.0.1',
    description=desc,
    long_description=long_desc,
    author='Rangertaha',
    author_email='rangertaha@gmail.com',
    maintainer='Rangertaha',
    maintainer_email='rangertaha@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    package_data={'delastic': ['templates/delastic/*.html']},
)
