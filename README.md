# pysetns
[![PyPI](https://img.shields.io/pypi/v/pysetns)](https://pypi.org/project/pysetns/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pysetns)](https://pypi.org/project/pysetns/)
[![PyPI - License](https://img.shields.io/pypi/l/pysetns)](https://github.com/baskiton/pysetns/blob/main/LICENSE)

Python wrapper for setns Linux syscall.\
See [setns manpage][man_setns] for more details.

## Requirements
 * Python 3.6+

## Installing
`pip install pysetns`

## Building
To build for your platform:
```
python -m build
pip install dist/<target_tar or wheel>
```

## Usage
See [examples][examples] directory

[man_setns]: https://man7.org/linux/man-pages/man2/setns.2.html
[examples]: https://github.com/baskiton/pysetns/blob/main/examples
