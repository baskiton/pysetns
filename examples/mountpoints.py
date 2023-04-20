#!/usr/bin/env python3

import errno
import os
import sys

import pysetns


def foo(ns):
    path = '/proc/%s/mounts' % ns.target_pid
    print(pid, pysetns.get_ns_string(ns.namespaces))

    if not os.path.exists('/proc'):
        err_code = errno.EAGAIN if ns.namespaces & pysetns.NS_MNT else errno.ENOENT
        print('[NS] "/proc" is not found. retry', file=sys.stderr)
        return err_code
    if not os.path.exists(path):
        path = '/proc/self/mounts'
    if not os.path.exists(path):
        print('[NS] Path is not exist for pid=%s: "%s"' % (ns.target_pid, path), file=sys.stderr)
        return errno.ENOENT
    for m in open(path).readlines():
        dev, mntp, tfs, opts, freq, passno = m.split()
        print('[NS] mntp=%s', mntp)


def bar(pid, namespaces):
    ns = pysetns.Namespace(pid, namespaces, keep_caps=True)
    ns.enter(foo, ns)
    for nst, msg in ns.errors.items():
        print('[NS] ERROR: <%s> %s' % (pysetns.get_ns_string(nst).upper(), msg), file=sys.stderr)
    return ns.retry


if __name__ == '__main__':
    pid = os.getpid()
    if bar(pid, pysetns.NS_MNT | pysetns.NS_PID | pysetns.NS_USER):
        bar(pid, pysetns.NS_PID | pysetns.NS_USER)
