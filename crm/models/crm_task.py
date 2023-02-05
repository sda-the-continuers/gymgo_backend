from django.db import models

from crm.enums import CRM_TASK_STATES, CRM_TASK_STATE_NOT_SEEN
from utility.models import HistoricalBaseModel


class CRMTask(HistoricalBaseModel):

    task_type = models.ForeignKey(
        to='crm.CRMTaskType',
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='نوع وظیفه',
    )

    customer = models.ForeignKey(
        to='crm.CRMAccount',
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='مشتری مربوطه'
    )

    description = models.TextField(
        verbose_name='توضیحات وظیفه'
    )

    state = models.CharField(
        max_length=64,
        choices=CRM_TASK_STATES,
        verbose_name='وضعیت',
        default=CRM_TASK_STATE_NOT_SEEN,
    )

    def __str__(self):
        return "id: %s - Task type: %s - state: %s" % (self.id, self.task_type, self.state)

    class Meta:
        verbose_name = 'وظیفه سی‌آرام'
        verbose_name_plural = 'وظایف سی‌آرام'

