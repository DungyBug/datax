def predict(array, i):
    if i < 2:
        return 0

    return (array[i - 1] - array[i - 2]) * 2 + array[i - 2]


def delta(array, i):
    if i < 1:
        return 0

    return array[i - 1]


def get_unawares(data):
    unawares = []

    for i in range(len(data)):
        prediction = predict(data, i)

        unawares.append(abs(prediction - data[i]))

    return unawares


def percentile(data, p: int):
    return sorted(data)[int(len(data) * p / 100)]


def detect_anomalies(data: list, chunk_size: int = 1000):
    out = (
        set(),
        set()
    )

    unawares = get_unawares(data)

    for i in range(max(len(unawares) - chunk_size, 1)):
        chunk = unawares[i:i+chunk_size]

        threeshold = percentile(chunk, 90)

        for j in range(len(chunk)):
            if chunk[j] > threeshold * 3:
                out[0].add(i + j)
            elif chunk[j] > threeshold * 2:
                out[1].add(i + j)

    # threeshold = percentile(unawares, 90)

    # for i in range(len(unawares)):
    #     if unawares[i] >= threeshold * 3:
    #         out[0].append(i)
    #     elif unawares[i] >= threeshold * 2:
    #         out[1].append(i)

    return out
