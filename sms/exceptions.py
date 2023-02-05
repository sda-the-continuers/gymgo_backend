import typing
from abc import ABC

if typing.TYPE_CHECKING:
    from sms.models import GymtimeSMSInterface
    from kavenegar import HTTPException, APIException


class GymTimeSMSException(Exception, ABC):
    sms: 'GymtimeSMSInterface'
    error: typing.Union['HTTPException', 'APIException']

    def __init__(self, sms, error, *args, **kwargs):
        self.sms = sms
        self.error = error
        super().__init__(
            f'Problem in {self.__class__.__name__} object with id {self.sms.id} and the cause was: {str(self.error)}',
            *args, **kwargs
        )
