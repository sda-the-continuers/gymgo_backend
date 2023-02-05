from django.core.exceptions import ValidationError
from django.db import models


class ClubRelatedMixin(models.Model):
    club = models.ForeignKey(
        to='gym.Club',
        on_delete=models.CASCADE,
        verbose_name='باشگاه مخاطبین مربوطه'
    )

    contacts = models.ManyToManyField(
        to='gym.ClubContact',
        verbose_name='مخاطبین',
    )

    def clean(self, validation_error_class=ValidationError):
        super().clean()
        if self.contacts.exclude(club=self.club).exists():
            raise validation_error_class({'contacts': ['فقط با مخاطبین باشگاه خودتان کار داشته باشید!']})

    class Meta:
        abstract = True
