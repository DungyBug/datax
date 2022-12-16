from pyspark import RDD


def get_count_by(log: RDD, index: int) -> RDD:
    def get_count(line):
        nonlocal index

        return (line[index], 1)

    return log.map(get_count) \
        .reduceByKey(lambda a, b: a + b)
