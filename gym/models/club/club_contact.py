from django.db import models

from utility.models import HistoricalBaseModel


class ClubContact(HistoricalBaseModel):

    club = models.ForeignKey(
        to='gym.Club',
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='باشگاه مخاطبین مربوطه'
    )

    full_name = models.CharField(
        verbose_name='نام کامل',
        max_length=256,
    )

    phone_number = models.CharField(
        max_length=32,
        verbose_name='شماره همراه',
    )

    athlete = models.ForeignKey(
        to='account.Athlete',
        on_delete=models.CASCADE,
        related_name='club_contacts',
        verbose_name='مجموعه ورزشی مربوطه',
        null=True, blank=True,
    )

    def before_create(self):
        from account.models import Athlete
        if athlete := Athlete.objects.filter(phone_number=self.phone_number).first():
            self.athlete = athlete

    class Meta:
        verbose_name = 'مخاطب باشگاه'
        verbose_name_plural = 'مخاطبین باشگاه'
        unique_together = ('club', 'phone_number', )


