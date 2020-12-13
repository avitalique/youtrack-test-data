from datetime import datetime, timedelta
import random


def get_datetime_list(length, years_ago=4):
    """Generate a list of datetime objects"""
    end = datetime.now()
    start = datetime.now() - timedelta(days=365 * random.randint(1, years_ago))

    datetime_list = []
    for i in range(0, length):
        datetime_list.append(get_random_date(start, end))
    datetime_list.sort()

    return datetime_list


def get_random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
