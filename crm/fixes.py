from django.db import transaction

from crm.enums import CRM_TASK_TYPES
from crm.models import CRMTaskType


def create_default_crm_task_types():
    with transaction.atomic():
        for crm_task_type in CRM_TASK_TYPES:
            file = open(f'templates/{crm_task_type[2]}')
            CRMTaskType.objects.get_or_create(
                name=crm_task_type[0],
                defaults=dict(
                    title=crm_task_type[1],
                    description_template=file.read()
                )
            )
