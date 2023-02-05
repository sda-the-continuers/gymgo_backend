from typing import List

from django.db import models

from sms.enums import KAVENEGAR_LIMITS, KAVENEGAR_MESSAGE_LENGTH_LIMIT, KAVENEGAR_RECEPTORS_LIMIT
from sms.models import GymtimeSMSInterface
from sms.negar import GymtimeNegar


class GymtimeSimpleSMS(GymtimeSMSInterface):
    message = models.TextField(
        verbose_name='متن پیام',
    )
    receptors: List[str] = []

    def get_receptors(self) -> List[str]:
        return self.receptors

    def validate(self):
        validation = super().validate()
        receptors = self.get_receptors()

        if not receptors:
            validation.add_validation_error('شماره تلفنی برای ارسال پیام داده نشده است.')

        has_wrong_phone_number = False
        for receptor in receptors:
            if not self.validate_phone_number(receptor):
                has_wrong_phone_number = True
                validation.add_validation_error('شماره تلفن {} اشتباه است!'.format(receptor))

        if has_wrong_phone_number:
            validation.add_validation_error(self.WRONG_PHONE_NUMBER_ERRORS)

        if len(self.message) > KAVENEGAR_LIMITS[KAVENEGAR_MESSAGE_LENGTH_LIMIT]:
            validation.add_validation_error('حداکثر تعداد کارکتر پیام {} حرف است'.format(
                KAVENEGAR_LIMITS[KAVENEGAR_MESSAGE_LENGTH_LIMIT]
            ))

        if len(receptors) > KAVENEGAR_LIMITS[KAVENEGAR_RECEPTORS_LIMIT]:
            validation.add_validation_error('حداکثر تعداد مخاطبین {} است'.format(
                KAVENEGAR_LIMITS[KAVENEGAR_RECEPTORS_LIMIT]
            ))

        return validation

    def send(self):
        return GymtimeNegar.send(self.get_receptors(), self.message)

    @property
    def try_gymtime_sms(self):
        from sms.models import GymtimeSMS
        if isinstance(self, GymtimeSMS):
            return self
        try:
            return self.gymtimesms
        except:
            return None

    @property
    def try_club_sms(self):
        from gym.models import ClubSMS
        if isinstance(self, ClubSMS):
            return self
        try:
            return self.clubsms
        except:
            return None

    @property
    def try_club_sms_for_discount(self):
        from gym.models import ClubSMSForDiscount
        if isinstance(self, ClubSMSForDiscount):
            return self
        try:
            return self.clubsmsfordiscount
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_club_sms_for_discount or self.try_club_sms or self.try_gymtime_sms

    class Meta:
        verbose_name = 'پیامک معمولی'
        verbose_name_plural = 'پیامک‌های معمولی'
