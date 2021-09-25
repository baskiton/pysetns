#define _GNU_SOURCE
#include <Python.h>
#include <sched.h>
#include <linux/sched.h>


PyDoc_STRVAR(ext__doc__,
"Wrapper for setns syscall.\n");

#define AddZeroMacro(m, c) PyModule_AddIntConstant(m, #c, 0)

PyDoc_STRVAR(setns__doc__,
"setns(fd: int, nstype: int) -> None\n"
"\n"
"Wrapper for setns syscall.\n"
"See the manpage for setns for more details.\n"
"\n"
"Raises:\n"
"    OSError: Raised when setns sets errno.\n");
static PyObject *
PySetns(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"fd", "nstype", NULL};
    int fd = -1;
    int nstype = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ii", kwlist,
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
        "ext",          /* m_name */
        ext__doc__,     /* m_doc */
        0,              /* m_size */
        ext_methods,    /* m_methods */
        NULL,           /* m_reload */
        NULL,           /* m_traverse */
        NULL,           /* m_clear */
        NULL            /* m_free */
};

PyMODINIT_FUNC
PyInit_ext(void)
{
    PyObject *module = PyModule_Create(&moduledef);
    if (module == NULL) {
        return NULL;
    }

#ifdef CLONE_NEWTIME
    PyModule_AddIntMacro(module, CLONE_NEWTIME);
#else
# warning "CLONE_NEWTIME macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWTIME);
#endif /* CLONE_NEWTIME */
#ifdef CLONE_NEWNS
    PyModule_AddIntMacro(module, CLONE_NEWNS);
#else
# warning "CLONE_NEWNS macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWNS);
#endif /* CLONE_NEWNS */
#ifdef CLONE_NEWCGROUP
    PyModule_AddIntMacro(module, CLONE_NEWCGROUP);
#else
# warning "CLONE_NEWCGROUP macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWCGROUP);
#endif /* CLONE_NEWCGROUP */
#ifdef CLONE_NEWUTS
    PyModule_AddIntMacro(module, CLONE_NEWUTS);
#else
# warning "CLONE_NEWUTS macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWUTS);
#endif /* CLONE_NEWUTS */
#ifdef CLONE_NEWIPC
    PyModule_AddIntMacro(module, CLONE_NEWIPC);
#else
# warning "CLONE_NEWIPC macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWIPC);
#endif /* CLONE_NEWIPC */
#ifdef CLONE_NEWUSER
    PyModule_AddIntMacro(module, CLONE_NEWUSER);
#else
# warning "CLONE_NEWUSER macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWUSER);
#endif /* CLONE_NEWUSER */
#ifdef CLONE_NEWPID
    PyModule_AddIntMacro(module, CLONE_NEWPID);
#else
# warning "CLONE_NEWPID macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWPID);
#endif /* CLONE_NEWPID */
#ifdef CLONE_NEWNET
    PyModule_AddIntMacro(module, CLONE_NEWNET);
#else
# warning "CLONE_NEWNET macro not found. Set to 0"
    AddZeroMacro(module, CLONE_NEWNET);
#endif /* CLONE_NEWNET */

    return module;
}
