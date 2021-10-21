#define _GNU_SOURCE
#include <Python.h>
#include <sched.h>
#include <linux/sched.h>


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

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i|i", kwlist,
                                     &fd, &nstype)) {
        return NULL;
    }

    if (setns(fd, nstype)) {
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    Py_RETURN_NONE;
}

static PyMethodDef ext_methods[] = {
        {"setns", (PyCFunction)PySetns, METH_VARARGS | METH_KEYWORDS, setns__doc__},
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
