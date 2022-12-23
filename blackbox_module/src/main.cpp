#define PY_SSIZE_T_CLEAN
#define PY_NO_LINK_LIB
#include "blackbox.h"

extern "C"
{
    /*
    ***************************************************
    **  Export functions
    ***************************************************
    */

    static struct PyMethodDef blackbox_methods[] = {
        {"delta_difference", (PyCFunction)anomaly_detector_delta_difference, METH_VARARGS, PyDoc_STR("blackbox.delta_difference(values: list[float|int], chunk_size: int = 1000): Detect anomalies in list of values")},
        {"linear_difference", (PyCFunction)anomaly_detector_linear_difference, METH_VARARGS, PyDoc_STR("blackbox.linear_difference(values: list[float|int], chunk_size: int = 1000): Detect anomalies in list of values")},
        {NULL, NULL, 0, NULL}};

    static struct PyModuleDef blackboxmodule = {
        .m_base = PyModuleDef_HEAD_INIT,
        .m_name = "blackbox",
        .m_doc = "Library for fast anomaly detection",
        .m_size = -1,
        .m_methods = blackbox_methods};

    PyMODINIT_FUNC
    PyInit_blackbox(void)
    {
        PyObject *m;

        m = PyModule_Create(&blackboxmodule);

        if (m == NULL)
            return NULL;

        return m;
    }
}