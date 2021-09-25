# coding: utf-8

__all__ = ('__version__', 'NS_TIME', 'NS_MNT', 'NS_CGROUP', 'NS_UTS',
           'NS_IPC', 'NS_USER', 'NS_PID', 'NS_NET', 'NS_ALL',
           'UserNamespaceWarning', 'Namespace', 'get_ns_string')

import errno
import os

from typing import Callable, Union, Iterable

from . import ext

__version__ = '0.1.0'

NS_TIME = ext.CLONE_NEWTIME     # time namespace (since Linux 5.8)
NS_MNT = ext.CLONE_NEWNS        # mount namespace group (since Linux 3.8)
NS_CGROUP = ext.CLONE_NEWCGROUP # cgroup namespace (since Linux 4.6)
NS_UTS = ext.CLONE_NEWUTS       # utsname namespace (since Linux 3.0)
NS_IPC = ext.CLONE_NEWIPC       # ipc namespace (since Linux 3.0)
NS_USER = ext.CLONE_NEWUSER     # user namespace (since Linux 3.8)
NS_PID = ext.CLONE_NEWPID       # pid namespace (since Linux 3.8)
NS_NET = ext.CLONE_NEWNET       # network namespace (since Linux 3.0)
NS_ALL = NS_MNT | NS_USER | NS_PID | NS_NET | NS_UTS | NS_IPC | NS_CGROUP | NS_TIME

_NS_NAMES = {
    # Order is very important here! NS_USER should always be last!
    NS_CGROUP: 'cgroup',
    NS_IPC: 'ipc',
    NS_UTS: 'uts',
    NS_NET: 'net',
    NS_PID: 'pid',
    NS_MNT: 'mnt',
    NS_TIME: 'time',
    NS_USER: 'user',
}

_OFLAGS = os.O_RDONLY | os.O_NONBLOCK | os.O_NOCTTY | getattr(os, 'O_CLOEXEC', 0o2000000)


def get_ns_string(ns_types: int) -> str:
    res = []
    for k, v in _NS_NAMES.items():
        if k & ns_types:
            res.append(v)
    return '|'.join(res)


class UserNamespaceWarning(Warning):
    def __init__(self, gid: int, uid: int, pid: Union[int, str]):
        self.message = (f'Further work will be under the *USER* namespace '
                        f'with rights of the user {gid}:{uid} of pid {pid}!')
        super(UserNamespaceWarning, self).__init__(self.message)


class Namespace:
    def __init__(self, target_pid: Union[int, str], ns_types: int = NS_ALL,
                 target_gid: int = 0, target_uid: int = 0, do_fork: int = False, true_user: int = False):
        if (isinstance(target_pid, int) or target_pid.isdigit()) and int(target_pid) <= 0:
            raise ValueError('Invalid target PID')
        if not NS_ALL & ns_types:
            raise TypeError('Invalid namespace types')

        self.errors = {}
        self.retry = False
        self.target_pid = target_pid
        proc_st = os.stat(f'/proc/{self.target_pid}')
        self.target_gid = target_gid or proc_st.st_gid
        self.target_uid = target_uid or proc_st.st_uid
        self.true_user = true_user

        self.parent_ns_files = {nstype: self._get_nsfd('self', name)
                                for nstype, name in _NS_NAMES.items()
                                if nstype & ns_types}
        if ns_types & NS_USER and self._disallow_user_ns(target_pid):
            self._close_fds(self.parent_ns_files.pop(NS_USER))
        self.target_ns_files = {nstype: self._get_nsfd(target_pid, name)
                                for nstype, name in _NS_NAMES.items()
                                if nstype in self.parent_ns_files
                                and self.parent_ns_files[nstype] != -1}
        self.namespaces = ns_types & NS_USER
        for t_nstype, t_fd in self.target_ns_files.items():
            if t_fd != -1:
                self.namespaces |= t_nstype
            else:
                for p_nstype, p_fd in self.parent_ns_files.items():
                    if p_nstype == t_nstype:
                        self._close_fds(p_fd)
                        break
        self.do_fork = do_fork or self.namespaces & (NS_USER | NS_PID)
        self.fork = -1

    def enter(self, target: Callable, args=(), kwargs={}) -> None:
        if not isinstance(target, Callable):
            raise TypeError('target is not callable')
        args = tuple(args)
        kwargs = dict(kwargs)

        for ns, fd in self.target_ns_files.copy().items():
            if ns == NS_USER and not self.true_user:
                continue
            try:
                if fd > 0:
                    ext.setns(fd, ns)
            except OSError as e:
                # TODO: log it
                self.errors[ns] = e
                self._close_fds(fd)
                self._close_fds(self.parent_ns_files[ns])
                if ns == NS_USER:
                    self.target_ns_files[NS_USER] = self.parent_ns_files[NS_USER] = -1
                else:
                    self.target_ns_files.pop(ns)
                    self.parent_ns_files.pop(ns)
                    self.namespaces &= ~ns
        if not self.namespaces:
            return
        if self.do_fork:
            self.fork = os.fork()
            if self.fork:
                return
            else:
                if self.namespaces & NS_USER:
                    os.setgid(self.target_gid)
                    os.setuid(self.target_uid)
        exitcode = 0
        try:
            exitcode = target(*args, **kwargs)
        finally:
            self.exit(exitcode)

    def exit(self, errcode: int = 0) -> None:
        uerr = 0
        if self.do_fork and self.fork != -1:
            if self.fork:
                _, status = os.wait()
                if status >> 8 == errno.EAGAIN:
                    self.retry = True
                self.fork = -1
            else:
                os._exit(errcode or 0)
        if self.namespaces & NS_USER and self.true_user:
            uerr = 1
        else:
            for ns, fd in reversed(self.parent_ns_files.items()):
                if ns == NS_USER:
                    continue
                try:
                    if fd > 0:
                        ext.setns(fd, ns)
                except OSError as e:
                    # further work is strictly prohibited!
                    # the entire parent process must be terminated!
                    self._close_fds(fd)
                    self.parent_ns_files[ns] = -1
                    self.namespaces &= ~ns
                    e.strerror = f'{e.strerror} when exiting from "{_NS_NAMES[ns]}" namespace. ' \
                                 f'Further work is impossible!'
                    raise
        self._close_fds(self.parent_ns_files.values())
        self._close_fds(self.target_ns_files.values())
        if uerr:
            self.parent_ns_files.clear()
            self.target_ns_files.clear()
            raise UserNamespaceWarning(self.target_gid, self.target_uid, self.target_pid)
        else:
            self.parent_ns_files = dict.fromkeys(self.parent_ns_files, -1)
            self.target_ns_files = dict.fromkeys(self.target_ns_files, -1)

    @staticmethod
    def _get_nsfd(pid: Union[int, str], ns_str: str) -> int:
        return os.open(f'/proc/{pid}/ns/{ns_str}', _OFLAGS)

    @staticmethod
    def _disallow_user_ns(target_pid) -> bool:
        # It is not permitted to use setns(2) to reenter the caller's current user namespace
        parent_ino = os.stat(f'/proc/{os.getpid()}/ns/user').st_ino
        target_ino = os.stat(f'/proc/{target_pid}/ns/user').st_ino
        return parent_ino == target_ino

    @staticmethod
    def _close_fds(fds: Union[int, Iterable]) -> None:
        if isinstance(fds, Iterable):
            for fd in fds:
                Namespace._close_fds(fd)
        else:
            try:
                os.close(fds)
            except OSError:
                pass
