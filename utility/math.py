import math


def round_to_number(number, round_target, round_method=math.ceil) -> int:
    return int(round_method(number / round_target)) * round_target


def round_to_thousand(number, round_method=math.ceil) -> int:
    return round_to_number(number, round_target=1000, round_method=round_method)