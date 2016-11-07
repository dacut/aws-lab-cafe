#!/usr/bin/env python2.7
import logging
from setuptools import setup

logging.basicConfig(level=logging.DEBUG)

setup(
    name="amzn-linux-mirror",
    version="1.0",
    py_modules=["hpclab"],
    install_requires=[
        "boto3>=1.0",
        "Flask>=0.11",
        "Flask-Login>=0.4",
    ],

    # PyPI information
    author="David Cuthbert",
    author_email="dacut@kanga.org",
    description="Portable HPC lab portal",
    license="BSD",
    url="https://github.com/dacut/hpc-lab-maker",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[],
    zip_safe=False,
)
