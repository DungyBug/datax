from datetime import date, timedelta


def to_string(dt: date):
    day = str(dt.day).rjust(2, '0')
    month = str(dt.month).rjust(2, '0')
    year = str(dt.year)

    return f"{year}-{month}-{day}"


def date_range(start, end):
    out = list()

    delta = end - start

    for i in range(delta.days + 1):
        day = start + timedelta(days=i)

        out.append(to_string(day))

    return out


def dttable_to_list(dttable: list[tuple[int, int]]):
    out = [dttable[0][1]]

    for i, value in enumerate(dttable):
        for _ in range(dttable[i - 1][0], value[0] - 1):
            out.append(0)

        out.append(value[1])

    return out
