#include <iostream>
#include <vector>
#include <set>
#include "linear_difference.h"
#include "../../utils.h"
using namespace std;

double predict(double prev, double current)
{
    return (current - prev) * 2 + prev;
}

double *get_prediction_deltas(double *array, unsigned long long size)
{
    double *deltas = new double[size];

    deltas[0] = array[0];

    for (unsigned long long i = 2; i < size; i++)
    {
        deltas[i] = abs(array[i] - predict(array[i - 2], array[i - 1]));
    }

    return deltas;
}

extern "C"
{
    PyObject *anomaly_detector_linear_difference(PyObject *self, PyObject *args)
    {
        unsigned long long chunkSize = 1000;
        PyObject *valuesList;

        if (!PyArg_ParseTuple(args, "O|K", &valuesList, &chunkSize))
        {
            PyErr_SetString(PyExc_TypeError, "blackbox.linear_difference(values: list[float|int], chunk_size: int = 1000): Expected one list of floats or ints.");
            return NULL;
        }

        // ********************************************
        // * Check, that provided "valuesList" has list or tuple type
        // ********************************************
        if (!PyList_Check(valuesList) && !PyTuple_Check(valuesList))
        {
            PyTypeObject *type = (PyTypeObject *)PyObject_Type(valuesList);
            char errorMessageBuffer[1024];

            sprintf(errorMessageBuffer, "blackbox.linear_difference(values: list[float|int], chunk_size: int = 1000): Expected \"list\" or \"tuple\" in \"values\", but got \"%s\".", type->tp_name);

            PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
            return NULL;
        }

        // ********************************************
        // * Copy all values to array of doubles
        // ********************************************
        unsigned long long size = PySequence_Fast_GET_SIZE(valuesList);
        double *values = new double[size];

        // Clamp chunkSize to size of array to avoid bugs
        chunkSize = min(chunkSize, size);

        for (unsigned long long i = 0; i < size; i++)
        {
            PyObject *item = PySequence_Fast_GET_ITEM(valuesList, i);

            if (PyLong_Check(item))
            {
                values[i] = PyLong_AsDouble(item);
            }
            else if (PyFloat_Check(item))
            {
                values[i] = PyFloat_AS_DOUBLE(item);
            }
            else
            {
                delete[] values;

                PyTypeObject *type = (PyTypeObject *)PyObject_Type(item);
                char errorMessageBuffer[1024];

                sprintf(errorMessageBuffer, "blackbox.linear_difference(values: list[float|int], chunk_size: int = 1000): Expected \"float\" or \"int\" in \"values[%lli]\", but got \"%s\".", i, type->tp_name);

                PyErr_SetString(PyExc_TypeError, errorMessageBuffer);
                return NULL;
            }
        }

        // ********************************************
        // * Find anomalies
        // ********************************************
        double *deltas = get_prediction_deltas(values, size);

        set<unsigned long long> criticalAnomalies;
        set<unsigned long long> minorAnomalies;

        double *chunk = new double[chunkSize];

        for (unsigned long long i = 0; i < size - chunkSize + 1; i++)
        {
            // Fill in chunk
            for (unsigned long long j = 0; j < chunkSize; j++)
            {
                chunk[j] = deltas[i + j];
            }

            sort(chunk, &chunk[chunkSize]);

            double threeshold = PERCENTILE(chunk, chunkSize, 90);

            for (unsigned long long j = 0; j < chunkSize; j++)
            {
                if (deltas[i + j] > threeshold * 3.0)
                {
                    criticalAnomalies.insert(i + j);
                }
                else if (deltas[i + j] > threeshold * 2.0)
                {
                    minorAnomalies.insert(i + j);
                }
            }
        }

        delete[] chunk;
        delete[] values;
        delete[] deltas;

        PyObject *criticalAnomaliesList = PyList_New(criticalAnomalies.size());
        PyObject *minorAnomaliesList = PyList_New(minorAnomalies.size());

        // Temp variable to calculate currentIndex of array
        // Used for both "criticalAnomaliesList" and "minorAnomaliesList"
        unsigned long long currentIndex = 0;

        // Fill in "criticalAnomaliesList"
        for (const unsigned long long &i : criticalAnomalies)
        {
            PyList_SET_ITEM(criticalAnomaliesList, currentIndex, PyLong_FromUnsignedLongLong(i));

            currentIndex++;
        }

        currentIndex = 0;

        // Fill in "minorAnomaliesList"
        for (const unsigned long long &i : minorAnomalies)
        {
            PyList_SET_ITEM(minorAnomaliesList, currentIndex, PyLong_FromUnsignedLongLong(i));

            currentIndex++;
        }

        PyObject *outTuple = PyTuple_Pack(2, criticalAnomaliesList, minorAnomaliesList);

        return outTuple;
    }
}