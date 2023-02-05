from django.db import models

from crm.enums import TICKET_STATES, TICKET_STATE_NOT_SEEN
from utility.models import HistoricalBaseModel


class Ticket(HistoricalBaseModel):

    ticket_type = models.ForeignKey(
        to='crm.TicketType',
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name='نوع تیکت'
    )

    customer = models.ForeignKey(
        to='crm.CRMAccount',
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name='مشتری مربوطه'
    )

    state = models.CharField(
        max_length=64,
        choices=TICKET_STATES,
        default=TICKET_STATE_NOT_SEEN,
    )

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'


