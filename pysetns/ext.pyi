__all__ = ('setns', 'CLONE_NEWTIME', 'CLONE_NEWNS', 'CLONE_NEWCGROUP', 'CLONE_NEWUTS',
           'CLONE_NEWIPC', 'CLONE_NEWUSER', 'CLONE_NEWPID', 'CLONE_NEWNET',)

O_CLOEXEC: int
NS_INVALID : int
CLONE_NEWTIME : int
CLONE_NEWNS : int
CLONE_NEWCGROUP : int
CLONE_NEWUTS : int
CLONE_NEWIPC : int
CLONE_NEWUSER : int
CLONE_NEWPID : int
CLONE_NEWNET : int

def setns(fd: int, nstype: int = 0) -> None: ...
def setguid_keep_cap(gid: int, uid: int) -> None: ...
