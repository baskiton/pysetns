#!/usr/bin/env python3

import os
import sys

from setuptools import find_packages, setup, Extension


_cur_dir = os.path.dirname(os.path.abspath(__file__))


def get_file_content(rel_path):
    return open(os.path.join(_cur_dir, rel_path)).read()


ext = Extension(
    'pysetns.ext',
    sources=['src/ext.c'],
    py_limited_api=True,
)

add_opts = {'setup_requires': []}
if sys.version_info >= (3, 7):
    add_opts['setup_requires'].append('setuptools-git-versioning')
    add_opts['setuptools_git_versioning'] = {
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
    long_description=get_file_content('README.md'),
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
    python_requires='>=3',
    package_data={
        '': ['examples/*']
    },
    **add_opts,
)
