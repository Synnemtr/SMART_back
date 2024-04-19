from functools import reduce


def unique(list1):
    unique_list = reduce(lambda re, x: re+[x] if x not in re else re, list1, [])
    return unique_list
