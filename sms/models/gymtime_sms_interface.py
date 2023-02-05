import re
from typing import Union, List

from django.db import models
from django.utils import timezone
from kavenegar import HTTPException, APIException

from sms.enums import GYMTIME_SMS_STATE, GYMTIME_SMS_AWAITING_SENDING, GYMTIME_SMS_CANCELLED, GYMTIME_SMS_SENT
from sms.exceptions import GymTimeSMSException
from utility.mixins import StatefulModelMixin
from utility.models import HistoricalBaseModel


class GymtimeSMSValidationProof:

    def __init__(self):
        self.is_valid = True
        self.errors = []

    def add_validation_error(self, error: Union[str, List[str]]):
        self.is_valid = False
        if isinstance(error, List):
            self.errors.extend(error)
        else:
            self.errors.append(error)

    def to_internal_value(self):
        return self.is_valid, self.errors


class GymtimeSMSInterface(StatefulModelMixin, HistoricalBaseModel):

    def init_old_instance_fields(self):
        self._current_state = self.state

    state = models.CharField(
        choices=GYMTIME_SMS_STATE,
        max_length=16,
        verbose_name='منظور استفاده',
        default=GYMTIME_SMS_AWAITING_SENDING,
    )

    sent_at = models.DateTimeField(
        null=True, blank=True, verbose_name='زمان ارسال',
    )

    gymtime_errors = models.TextField(null=True, blank=True, verbose_name='ارورها')
    service_errors = models.TextField(null=True, blank=True, verbose_name='ارورها')

    # compile once, use many times in O(n)
    PHONE_NUMBER_REGEX = re.compile(r'^(0|(\+|00)98)?9\d{9}$')
    WRONG_PHONE_NUMBER_ERRORS = [
        'شماره تلفن داده شده باید به یکی از چهار فرمت زیر باشد:',
        '09121234567',
        '00989121234567',
        '+989121234567',
        '9121234567',
    ]

    @classmethod
    def validate_phone_number(cls, phone_number: str):
        return bool(cls.PHONE_NUMBER_REGEX.match(phone_number))

    def validate(self) -> GymtimeSMSValidationProof:
        return GymtimeSMSValidationProof()

    def send(self):
        raise NotImplementedError

    def validate_and_send(self, save=False):
        try:
            message = None
            is_valid, errors = self.validate().to_internal_value()
            if is_valid:
                message = self.send()
                self.state = GYMTIME_SMS_SENT
            else:
                self.gymtime_errors = '\n'.join(errors)
                self.state = GYMTIME_SMS_CANCELLED
            return message
        except (APIException, HTTPException) as e:
            self.service_errors = str(e)
            raise GymTimeSMSException(self, e)
        finally:
            if save:
                self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_transiting_to(GYMTIME_SMS_SENT):
            self.sent_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'پیامک جیم‌تایم'
        verbose_name_plural = 'پیامک‌های جیم‌تایم'
        abstract = True
