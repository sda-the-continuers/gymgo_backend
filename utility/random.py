import random
import string


def generate_random_number(length=6) -> str:
    letters = string.digits
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def generate_random_alphabetic_code(length) -> str:
    letters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def generate_random_string(
        length=6,
        digits=False,
        upper_case=False,
        lower_case=False,
        punctuation=False,
        custom_options: str = None,
):
    if not (digits or upper_case or lower_case or punctuation):
        return None
    options = ''
    if digits:
        options += string.digits
    if upper_case:
        options += string.ascii_uppercase
    if lower_case:
        options += string.ascii_lowercase
    if punctuation:
        options += string.punctuation
    options += custom_options or ''
    return ''.join(random.choice(options) for _ in range(length))
