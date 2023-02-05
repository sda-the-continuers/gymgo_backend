from typing import List

from django.db import models

from sms.models import GymtimeSMSInterface
from sms.negar import GymtimeNegar


class GymtimeLookupSMS(GymtimeSMSInterface):
    phone_number = models.CharField(
        max_length=32,
        verbose_name='شماره همراه',
    )

    tokens: List[str] = []

    template: str = ''

    def get_template(self) -> str:
        return self.template

    def get_tokens(self) -> List[str]:
        return self.tokens

    def validate(self):
        validation = super().validate()
        if not self.validate_phone_number(self.phone_number):
            validation.add_validation_error([
                'شماره تلفن {} اشتباه است!'.format(self.phone_number),
                *self.WRONG_PHONE_NUMBER_ERRORS
            ])

        tokens = self.get_tokens()
        if not isinstance(tokens, (list, tuple)) or not 1 <= len(tokens) <= 3:
            validation.add_validation_error('توکن‌ها باید حداقل ۱ و حداکثر ۳ عدد باشند.')

        if not self.get_template():
            validation.add_validation_error('باید تمپلیت ارسال پیام احراز هویت داده شود.')

        return validation

    def send(self):
        return GymtimeNegar.lookup(self.phone_number, self.get_template(), *self.get_tokens())

    class Meta:
        verbose_name = 'پیامک احراز هویت'
        verbose_name_plural = 'پیامک‌های احراز هویت'
