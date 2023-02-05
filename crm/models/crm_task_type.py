from django.db import models
from django.template import Template, Context

from utility.models import HistoricalBaseModel


class CRMTaskType(HistoricalBaseModel):

    name = models.CharField(
        max_length=256,
        unique=True,
        db_index=True,
        verbose_name='نام انگلیسی'
    )

    title = models.CharField(
        max_length=128,
        verbose_name='عنوان',
    )

    description_template = models.TextField(
        verbose_name='تمپلیت توضیحات'
    )

    @classmethod
    def create_task(cls, task_name, customer, **description_kwargs):
        from crm.models import CRMTask
        task_type: 'CRMTaskType' = cls.objects.get(task_name)
        return CRMTask.objects.create(
            task_type=task_type,
            customer=customer,
            description=Template(task_type.description_template).render(
                Context(description_kwargs)
            )
        )

    class Meta:
        verbose_name = 'نوع وظیفه سی‌آرام'
        verbose_name_plural = 'نوع وظایف سی‌آرام'

