from django.db import models


class PhoneNumberMixin(models.Model):

    phone_number = models.CharField(
        max_length=32,
        verbose_name='شماره همراه',
        unique=True,
    )

    def get_user_key(self):
        return f'{super().get_user_key()}-{self.phone_number}'

    def __str__(self):
        return "%s-%s" % (self.id, self.phone_number)

    class Meta:
        abstract = True
