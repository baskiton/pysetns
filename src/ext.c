#define _GNU_SOURCE
#include <Python.h>
#include <sched.h>
#include <linux/sched.h>
#include <linux/capability.h>
#include <sys/prctl.h>
#include <syscall.h>


PyDoc_STRVAR(ext__doc__,
"Wrapper for setns syscall.\n");

#define EXT_ADD_ZERO_MACRO(name) PyModule_AddIntConstant(module, #name, 0)
#define EXT_ADD_INT_MACRO(name) PyModule_AddIntConstant(module, #name, name)

PyDoc_STRVAR(setns__doc__,
"setns(fd, nstype=0) -> None\n"
"\n"
"Wrapper for setns syscall.\n"
"See the manpage for setns for more details:\n"
"    https://man7.org/linux/man-pages/man2/setns.2.html\n"
"\n"
"Args:\n"
"    fd (int): Namespace file descriptor.\n"
"    nstype (int): Namespaces types bitwise flag.\n"
"\n"
"Raises:\n"
"    OSError: Raised when setns sets errno.\n");

static PyObject *
PySetns(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"fd", "nstype", NULL};
    int fd = -1;
    int nstype = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i|i:setns", kwlist,
                                     &fd, &nstype)) {
        return NULL;
    }

    if (setns(fd, nstype)) {
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    Py_RETURN_NONE;
}


static long
capget(cap_user_header_t header, cap_user_data_t dataptr)
{
    return syscall(SYS_capget, header, dataptr);
}

static long
capset(cap_user_header_t header, cap_user_data_t dataptr)
{
    return syscall(SYS_capset, header, dataptr);
}

typedef struct cap_s {
    struct __user_cap_header_struct hdr;
    struct __user_cap_data_struct data[_LINUX_CAPABILITY_U32S_3];
} cap_t;

PyDoc_STRVAR(setguid_keep_cap__doc__,
"setguid_keep_cap(gid: int, uid: int) -> None\n"
"\n"
"Set GID and UID with keep capabilities of the caller.\n"
"\n"
"Args:\n"
"    gid (int): Group ID\n"
"    uid (int): User ID\n"
"\n"
"Raises:\n"
"    OSError: Raised when error occured.\n");

static PyObject *
PySetguid_keep_cap(PyObject *self, PyObject *a, PyObject *kw)
{
    static char *kwlist[] = {"gid", "uid", 0};
    unsigned int gid, uid;

    if (!PyArg_ParseTupleAndKeywords(a, kw, "II:setguid_keep_cap", kwlist, &gid, &uid))
        return 0;

    cap_t cap = {
        .hdr.pid = getpid(),
        .hdr.version = _LINUX_CAPABILITY_VERSION_3,
    };

    if (prctl(PR_SET_KEEPCAPS, 1)
            || capget(&cap.hdr, cap.data)
            || setgid(gid)
            || setuid(uid)
            || capset(&cap.hdr, cap.data))
        return PyErr_SetFromErrno(PyExc_OSError);

    Py_RETURN_NONE;
}


static PyMethodDef ext_methods[] = {
        {"setns", (PyCFunction)PySetns, METH_VARARGS | METH_KEYWORDS, setns__doc__},
        {"setguid_keep_cap", (PyCFunction)PySetguid_keep_cap, METH_VARARGS | METH_KEYWORDS, setguid_keep_cap__doc__},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        .m_name = "ext",
        .m_doc = ext__doc__,
        .m_size = 0,
        .m_methods = ext_methods,
};

PyMODINIT_FUNC
PyInit_ext(void)
{
    PyObject *module = PyModule_Create(&moduledef);
    if (module == NULL) {
        return NULL;
    }

#ifdef CLONE_NEWIPC     // since Linux 3.0
    EXT_ADD_INT_MACRO(CLONE_NEWIPC);
    EXT_ADD_INT_MACRO(CLONE_NEWNET);
    EXT_ADD_INT_MACRO(CLONE_NEWUTS);
#else
    EXT_ADD_ZERO_MACRO(CLONE_NEWIPC);
    EXT_ADD_ZERO_MACRO(CLONE_NEWNET);
    EXT_ADD_ZERO_MACRO(CLONE_NEWUTS);
#endif // CLONE_NEWIPC (since Linux 3.0)

#ifdef CLONE_NEWNS      // since Linux 3.8
    EXT_ADD_INT_MACRO(CLONE_NEWNS);
    EXT_ADD_INT_MACRO(CLONE_NEWPID);
    EXT_ADD_INT_MACRO(CLONE_NEWUSER);
#else
    EXT_ADD_ZERO_MACRO(CLONE_NEWNS);
    EXT_ADD_ZERO_MACRO(CLONE_NEWPID);
    EXT_ADD_ZERO_MACRO(CLONE_NEWUSER);
#endif // CLONE_NEWNS (since Linux 3.8)

#ifdef CLONE_NEWCGROUP  // since Linux 4.6
    EXT_ADD_INT_MACRO(CLONE_NEWCGROUP);
#else
    EXT_ADD_ZERO_MACRO(CLONE_NEWCGROUP);
#endif // CLONE_NEWCGROUP (since Linux 4.6)

#ifdef CLONE_NEWTIME    // since Linux 5.8
    EXT_ADD_INT_MACRO(CLONE_NEWTIME);
#else
    EXT_ADD_ZERO_MACRO(CLONE_NEWTIME);
#endif // CLONE_NEWTIME (since Linux 5.8)

    return module;
}
