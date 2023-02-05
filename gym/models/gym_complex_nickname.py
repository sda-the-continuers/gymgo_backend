from django.db import models

from utility.models import BaseModel


class GymComplexNickname(BaseModel):

    gym_complex = models.ForeignKey(
        to='gym.GymComplex',
        on_delete=models.CASCADE,
        related_name='nicknames',
        verbose_name='مجموعه ورزشی'
    )

    nickname = models.CharField(
        max_length=512,
        verbose_name='نام مستعار',
    )

    def __str__(self):
        return f'{self.gym_complex.code}: {self.nickname}'

    class Meta:
        verbose_name = 'نام مستعار مجموعه ورزشی'
        verbose_name_plural = 'نام‌های مستعار مجموعه ورزشی'
