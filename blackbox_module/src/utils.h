#ifndef UTILS_H
#define UTILS_H
#define PERCENTILE_INDEX(size, p) ((size) * (p) / 100)
#define PERCENTILE(arr, size, p) (arr[(size) * (p) / 100])

double max(double a, double b);
double min(double a, double b);

#endif // UTILS_H