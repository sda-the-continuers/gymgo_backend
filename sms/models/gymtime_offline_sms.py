from abc import ABC
from typing import Type, Union

from django.forms import JSONField

from sms.enums import GYMTIME_SMS_SENT
from sms.models import GymtimeSimpleSMS, GymtimeSMSInterface, GymtimeLookupSMS
from utility.models import CreateHistoryModel


class GymtimeOfflineSMSLog(CreateHistoryModel):
    params = JSONField()

    class Meta:
        verbose_name = 'لاگ پیامک آفلاین جیم‌تایم'
        verbose_name_plural = 'لاگ‌های پیامک‌های آفلاین جیم‌تایم'


class GymtimeOfflineSMS(GymtimeSMSInterface):
    def get_log_params(self) -> dict:
        cls: Union[Type[GymtimeOfflineSimpleSMS], Type[GymtimeOfflineLookupSMS]] = self.__class__
        return {
            'class': cls.__name__,
            'class_verbose': cls.Meta.verbose_name,
        }

    def log(self) -> GymtimeOfflineSMSLog:
        raise GymtimeOfflineSMSLog.objects.create(params=self.get_log_params())

    def validate_and_send(self):
        message = super().validate_and_send()
        log = None
        if self.state == GYMTIME_SMS_SENT:
            log = self.log()
        return message, log

    class Meta:
        abstract = True


class GymtimeOfflineSimpleSMS(GymtimeSimpleSMS, GymtimeOfflineSMS):

    def __init__(self, receptors, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.receptors = receptors

    def get_log_params(self) -> dict:
        return {
            **super().get_log_params(),
            'receptors': self.get_receptors(),
            'message': self.message,
        }

    class Meta:
        abstract = True
        verbose_name = GymtimeSimpleSMS.Meta.verbose_name


class GymtimeOfflineLookupSMS(GymtimeLookupSMS, GymtimeOfflineSMS):
    def __init__(self, tokens, template, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokens = tokens
        self.template = template

    def get_log_params(self) -> dict:
        return {
            **super().get_log_params(),
            'phone_number': self.phone_number,
            'message': self.get_tokens(),
            'template': self.template,
        }

    class Meta:
        abstract = True
        verbose_name = GymtimeLookupSMS.Meta.verbose_name
