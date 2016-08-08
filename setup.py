#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='pyweibo',
    version='0.1',
    description='Sina Weibo Scraper',
    author='Charles Weng',
    author_email='mystery.wd@gmail.com',
    url='https://github.com/w1ndy/pyweibo',
    packages=['pyweibo'],
    packages_dir={'pyweibo': 'pyweibo'},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'geopy',
        'rsa',
        'pillow',
        'numpy'
    ]
)
