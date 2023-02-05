from django.db import models

from utility.models import BaseModel


class TicketMessageAttachment(BaseModel):
    ticket_message = models.OneToOneField(
        to='crm.TicketMessage',
        on_delete=models.CASCADE,
        related_name='attachment',
        verbose_name='پیام تیکت مربوطه'
    )

    file = models.FileField(
        upload_to='crm',
        verbose_name='فایل',
    )

    class Meta:
        verbose_name = 'ضمیمه پیام تیکت'
        verbose_name_plural = 'ضمایم پیام تیکت'
