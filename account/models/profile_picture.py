from django.db import models, transaction

from utility.models import CreateHistoryModel


class ProfilePicture(CreateHistoryModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_active = self.is_active

    account = models.ForeignKey(
        to='account.Account',
        on_delete=models.CASCADE,
        related_name='profile_pictures',
        verbose_name='صاحب عکس',
    )

    file = models.FileField(
        upload_to='profile_pictures',
        verbose_name='فایل',
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name='آیا فعال است؟'
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            super().save(force_insert, force_update, using, update_fields)
            if self.is_active and self.is_active != self._is_active:
                self.__class__.objects.filter(
                    account_id=self.account_id,
                    is_active=True,
                ).update(is_active=False)

    class Meta:
        verbose_name = 'عکس پروفایل'
        verbose_name_plural = 'عکس‌های پروفایل‌ها'
