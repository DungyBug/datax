from datetime import datetime, date
from pyspark import SparkContext, SparkConf, RDD
import matplotlib.pyplot as plt
from test import *
from utils import date_range, dttable_to_list
from metrics import get_count_by
import blackbox

# *************************************
# Подготовка
# *************************************

DATES = date_range(date(2021, 12, 15), date(2022, 12, 13))


conf = SparkConf().setAppName("sparkapp").setMaster("local[6]")
sc = SparkContext(conf=conf)


def parse_log(line: str):
    return tuple(map(lambda x: x.split("=")[1], line.split()))


rdds: list[RDD] = list()

# Чтобы не ждать, пока просчитаются все даты, можно сделать так:
# for dt in DATES[:20]
for dt in DATES:
    rdd = sc.textFile("./project/" + dt) \
        .map(parse_log) \
        .filter(lambda x: x[0] == "context") \
        .map(lambda x: (x[0], x[1], x[2], x[3], x[4], int(int(x[5]) // 60), x[6]))

    rdds.append(rdd)


log = sc.union(rdds)

# *************************************
# Считаем количество действий
# *************************************

result = get_count_by(log, 5) \
    .sortByKey() \
    .collect()

data = dttable_to_list(result)

# *************************************
# Получаем аномалии и неожиданности
# *************************************

# Это необязательно, но помогает увидеть, насколько "неожиданным" было то или иное изменение графика
unawares = get_unawares(data)

print("calculating blackbox...")
print(datetime.now())

# Можно использовать blackbox.delta_difference(data)
# или detect_anomalies(data), если нет собранного blackbox
anomalies = blackbox.linear_difference(data)

print(datetime.now())
# print("calculating python implementation...")
# print(datetime.now())
# test_anomalies = detect_anomalies(data)
# print(datetime.now())

print("done!")
print("BlackBox:", anomalies)
# print("Python implementation:", test_anomalies)

# *************************************
# Визуализируем
# *************************************

plt.plot(range(len(unawares)), unawares, color="#f00", linewidth=0.5)
plt.plot(range(len(data)), data, color="#08f", linewidth=1)

for x in anomalies[0]:
    plt.axvline(x, color="#f00", linestyle="dashed", linewidth=1)

for x in anomalies[1]:
    plt.axvline(x, color="#f80", linestyle="dashed", linewidth=0.5)

plt.show()
