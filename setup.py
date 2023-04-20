#!/usr/bin/env python3

import pathlib
import sys

from setuptools import find_packages, setup, Extension


MINIMAL_PY_VERSION = (3, 8)
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
    py_limited_api=True,
)

add_opts = {'setup_requires': []}
if sys.version_info >= (3, 7):
    add_opts['setup_requires'].append('setuptools-git-versioning')
    add_opts['setuptools-git-versioning'] = {
        'enabled': True,
        'template': '{tag}.{ccount}',
        'dev_template': '{tag}.{ccount}',
        'dirty_template': '{tag}.{ccount}',
    }

setup(
    name='pysetns',
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
    packages=find_packages(exclude=('docs', 'examples')),
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
    python_requires='>=3.8',
    package_data={
        '': ['examples/*']
    },
    **add_opts,
)
