#ifndef DELTA_DIFFERENCE_H
#define DELTA_DIFFERENCE_H

#include <Python.h>
#include <structmember.h>

extern "C"
{

    extern PyObject *anomaly_detector_delta_difference(PyObject *self, PyObject *args);
}

#endif // DELTA_DIFFERENCE_H