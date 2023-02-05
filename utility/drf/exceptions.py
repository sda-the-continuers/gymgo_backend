from functools import wraps

from rest_framework.exceptions import ValidationError
from django.core import exceptions as django_exceptions


def type_safe_exception_wrapper(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as e:
            raise ValidationError(e.args[0])
        except django_exceptions.ValidationError as e:
            raise ValidationError(e)
    return wrapped
