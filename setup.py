#!/usr/bin/env python3

import pathlib
import sys

from setuptools import find_packages, setup, Extension


MINIMAL_PY_VERSION = (3, 6)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('This app works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_file(rel_path):
    return (pathlib.Path(__file__).parent / rel_path).read_text('utf-8')


def get_version():
    for line in get_file('pysetns/__init__.py').splitlines():
        if line.startswith('__version__'):
            return line.split()[2][1:-1]


ext = Extension(
    'pysetns.ext',
    sources=['src/ext.c'],
)

setup(
    name='pysetns',
    version=get_version(),
    url='https://github.com/baskiton/pysetns',
    project_urls={
        'Source': 'https://github.com/baskiton/pysetns',
        'Bug Tracker': 'https://github.com/baskiton/pysetns/issues',
    },
    license='MIT',
    author='Alexander Baskikh',
    author_email='baskiton@gmail.com',
    description='Python wrapper for setns Linux syscall.',
    long_description=get_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
    ],
    ext_modules=[ext],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Operating System Kernels :: Linux',
    ],
    keywords='linux kernel namespace setns',
    python_requires='>=3.6',
    package_data={
        '': ['examples/*']
    }
)
