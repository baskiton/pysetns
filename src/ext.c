#define _GNU_SOURCE
#include <Python.h>
#include <sched.h>
#include <linux/sched.h>


PyDoc_STRVAR(ext__doc__,
"Wrapper for setns syscall.\n");

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

    PyModule_AddIntMacro(module, CLONE_NEWTIME);
    PyModule_AddIntMacro(module, CLONE_NEWNS);
    PyModule_AddIntMacro(module, CLONE_NEWCGROUP);
    PyModule_AddIntMacro(module, CLONE_NEWUTS);
    PyModule_AddIntMacro(module, CLONE_NEWIPC);
    PyModule_AddIntMacro(module, CLONE_NEWUSER);
    PyModule_AddIntMacro(module, CLONE_NEWPID);
    PyModule_AddIntMacro(module, CLONE_NEWNET);

    return module;
}
