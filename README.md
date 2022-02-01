# pysetns
[![PyPI](https://img.shields.io/pypi/v/pysetns)](https://pypi.org/project/pysetns/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pysetns)](https://pypi.org/project/pysetns/)
[![PyPI - License](https://img.shields.io/pypi/l/pysetns)](https://github.com/baskiton/pysetns/blob/main/LICENSE)

[![build](https://github.com/baskiton/pysetns/actions/workflows/build.yml/badge.svg)](https://github.com/baskiton/pysetns/actions/workflows/build.yml)
[![upload](https://github.com/baskiton/pysetns/actions/workflows/pypi-upload.yml/badge.svg)](https://github.com/baskiton/pysetns/actions/workflows/pypi-upload.yml)

`pysetns` - is a Python wrapper for the Linux `setns` system call.\
See the [manual][man_setns] for an introduction to `setns` and namespaces.

### IMPORTANT!
`setns` requires execution from **ROOT**!

## Requirements
 * Python 3.6+

## Installing
`pip install pysetns`

## Building
To build for your platform:
```sh
python -m build
pip install dist/<target_tar or wheel>
```

## Usage
See [examples][examples]

_class_ pysetns.**Namespace**(_*args, **kwargs_)

* **\_\_init\_\_**(_target_pid, ns_types=NS_ALL,
                   target_gid=None, target_uid=None, do_fork=False,
                   true_user=False, keep_caps=False_):
  * `target_pid (int | str)` The pid of the process whose namespace you want to access
  * `ns_types (int)` Namespace types to be accessed. These are bitwise. _NS_ALL_ included all of this:
    * _NS_TIME_ - time namespace (since Linux 5.8)
    * _NS_MNT_ - mount namespace group (since Linux 3.8)
    * _NS_CGROUP_ - cgroup namespace (since Linux 4.6)
    * _NS_UTS_ - utsname namespace (since Linux 3.0)
    * _NS_IPC_ - ipc namespace (since Linux 3.0)
    * _NS_USER_ - user namespace (since Linux 3.8)
    * _NS_PID_ - pid namespace (since Linux 3.8)
    * _NS_NET_ - network namespace (since Linux 3.0)
  * `target_gid (int)` and `target_uid (int)` The GID and UID of the user you want to access in `NS_USER` as.
If _None_, the GID and UID of the process owner will be used
  * `do_fork (bool)` Enter into the namespace in a separate process. If ns_type includes NS_USER or NS_PID,
entering into the namespace will be done in a separate process and `do_fork` value is ignored
  * `true_user (bool)` If _False_ (default), entering into _NS_USER_ will be done by simply switching to target
GID and UID (_target_gid_, _target_uid_), otherwise through a system call, but then returning from the namespace
will not be possible and the program will need to be terminated.
  * `keep_caps (bool)` Preserve **root** capabilities if you need to perform an action
on behalf of a user with administrator rights. Only relevant if _ns_types_ includes _NS_USER_


 * **enter**(_target, *args, **kwargs_)\
Enter into **namespace** and execute _target_ function with its _args_ and _kwargs_.
Exiting namespaces will happen automatically. But if this needs to be done inside the _target_ function,
pass the **namespace** object as one of the parameters to it and call the _exit()_ method.
If an error occurs while entering into **namespace**, it will be written to the _errors_ attribute in the format "_ns_type: error_",
and if it was not the only _ns_type_, work will continue.
Errors caused by the operation of the _target_ function will be ignored, so take care of them yourself.


 * **exit**(_errcode=0_)\
Exit from **namespace** and set the _errcode_ if required.
You usually don't need to call this function yourself.
If the _errcode_ is set to 11 (`EAGAIN`), the _retry_ attribute will be set to True.


**get_ns_string**(_ns_types_)\
&nbsp;&nbsp;&nbsp;&nbsp;Represents namespace types _ns_types_ in string view.


[man_setns]: https://man7.org/linux/man-pages/man2/setns.2.html
[examples]: https://github.com/baskiton/pysetns/blob/main/examples
