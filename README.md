# pysetns
[![pypi](https://img.shields.io/pypi/v/pysetns?logo=python&logoColor=white)](https://pypi.org/project/pysetns/)
[![downloads](https://img.shields.io/pypi/dm/pysetns?logo=python&logoColor=white)](https://pypi.org/project/pysetns/)
[![license](https://img.shields.io/pypi/l/pysetns?logo=open-source-initiative&logoColor=white)](https://github.com/baskiton/pysetns/blob/main/LICENSE)

[![build](https://img.shields.io/github/workflow/status/baskiton/pysetns/build?logo=github)](https://github.com/baskiton/pysetns/actions/workflows/build.yml)
[![upload](https://img.shields.io/github/workflow/status/baskiton/pysetns/upload?label=upload&logo=github)](https://github.com/baskiton/pysetns/actions/workflows/pypi-upload.yml)
[![docs](https://img.shields.io/readthedocs/pysetns?logo=readthedocs&logoColor=white)][documentation]

`pysetns` - is a Python wrapper for the Linux `setns` system call. \
See the [manpage][man_setns] for an introduction to `setns` and namespaces.

To detail see the [documentation][documentation]

### IMPORTANT!
`setns` required execution from **ROOT**!

## Requirements
 * Python 3.6+

## Installing
### Using PIP
```sh
$ pip install pysetns
```

### From sources
```sh
$ git clone https://github.com/baskiton/pysetns.git
$ cd pysetns
$ python setup.py install
```

## Usage
See [examples][examples]


[man_setns]: https://man7.org/linux/man-pages/man2/setns.2.html
[examples]: https://github.com/baskiton/pysetns/blob/main/examples
[documentation]: https://pysetns.readthedocs.io
