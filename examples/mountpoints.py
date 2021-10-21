#!/usr/bin/env python3

import errno
import os
import sys

import pysetns


def foo(ns: pysetns.Namespace):
    path = f'/proc/{ns.target_pid}/mounts'
    print(pid, pysetns.get_ns_string(ns.namespaces))

    if not os.path.exists('/proc'):
        err_code = errno.EAGAIN if ns.namespaces & pysetns.NS_MNT else errno.ENOENT
        print(f'[NS] "/proc" is not found. retry', file=sys.stderr)
        return err_code
    if not os.path.exists(path):
        path = '/proc/self/mounts'
    if not os.path.exists(path):
        print(f'[NS] Path is not exist for pid={ns.target_pid}: "{path}"', file=sys.stderr)
        return errno.ENOENT
    for m in open(path).readlines():
        dev, mntp, tfs, opts, freq, passno = m.split()
        print(f'[NS] {mntp=}')


def bar(pid, namespaces):
    ns = pysetns.Namespace(pid, namespaces)
    ns.enter(foo, args=(ns,))
    if ns.errors:
        print(f'NS errors: {ns.errors}')
    return ns.retry


if __name__ == '__main__':
    pid = 37
    if bar(pid, pysetns.NS_MNT | pysetns.NS_PID | pysetns.NS_USER):
        bar(pid, pysetns.NS_PID | pysetns.NS_USER)
