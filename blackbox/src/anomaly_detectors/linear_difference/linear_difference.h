#ifndef LINEAR_DIFFERENCE_H
#define LINEAR_DIFFERENCE_H

#include <Python.h>
#include <structmember.h>

extern "C"
{

    extern PyObject *anomaly_detector_linear_difference(PyObject *self, PyObject *args);
}

#endif // LINEAR_DIFFERENCE_H