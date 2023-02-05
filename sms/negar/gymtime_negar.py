import logging
from datetime import datetime
from functools import wraps
from typing import Union, List, Type

from django.conf import settings
from kavenegar import KavenegarAPI

logger = logging.getLogger(__name__)


class GymtimeNegarMeta(type):

    @staticmethod
    def get_wrapper():
        def negar_method_wrapper(fn):
            @wraps(fn)
            def negar_method_wrapped(*args, **kwargs):
                if settings.FEATURE_FLAGS['NEGAR_FEATURE_FLAG']:
                    return fn(*args, **kwargs)
                logger.error(
                    'Could Not Use Negar. The Feature Flag Is Off!\n'
                    'Method Args: {}\n'
                    'Method Kwargs: {}\n'.format(args, kwargs),
                    exc_info=True
                )

            return negar_method_wrapped
        return negar_method_wrapper

    def __new__(cls, name, bases, dictionary):
        result: Type[GymtimeNegar] = type.__new__(cls, name, bases, dictionary)
        wrapper = cls.get_wrapper()
        for method in result.negar_methods:
            wrapped = wrapper(getattr(result, method))
            setattr(result, method, wrapped)
        return result


class GymtimeNegar(metaclass=GymtimeNegarMeta):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

    negar_methods = [
        'send',
        'lookup',
    ]

    @staticmethod
    def clean_api_kwargs(**kwargs):
        cleaned_kwargs = {}
        for key, val in kwargs.items():
            if val is not None:
                cleaned_kwargs[key] = val
        return cleaned_kwargs

    @classmethod
    def send(
            cls, receptor: Union[str, List[str]], message: str,
            sender: str = None, date: datetime = None, type: str = None, hide: bool = None,
    ):
        return cls.api.sms_send(
            cls.clean_api_kwargs(receptor=receptor, message=message, sender=sender, date=date, type=type, hide=hide)
        )

    @classmethod
    def lookup(
            cls, receptor: str, template: str, token: str,
            token2: str = None, token3: str = None, type: str = None,
    ):
        return cls.api.verify_lookup(
            cls.clean_api_kwargs(
                receptor=receptor, template=template, token=token, token2=token2, token3=token3, type=type
            )
        )
