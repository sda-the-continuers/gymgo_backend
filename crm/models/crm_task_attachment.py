from django.db import models

from utility.models import BaseModel


class CRMTaskAttachment(BaseModel):

    crm_task = models.ForeignKey(
        to='crm.CRMTask',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='وظیفه مربوطه',
    )

    file = models.FileField(
        upload_to='crm',
        verbose_name='فایل',
    )

    class Meta:
        verbose_name = 'ضمیمه وظیفه سی‌آرام'
        verbose_name_plural = 'ضمایم وظیفه سی‌آرام'
