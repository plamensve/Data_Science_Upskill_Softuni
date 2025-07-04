import re

import numpy as np

cur_value = '25lbs,kg'


def get_value(x):
    pattern = r"(\d+)"
    matches = re.findall(pattern, x)

    if 'kg' in x:
        return int(matches[0])
    elif 'lbs' in x:
        return round(int(matches[0]) * 0.453592, 2)
    else:
        return int(matches[0])


print(get_value(cur_value))
