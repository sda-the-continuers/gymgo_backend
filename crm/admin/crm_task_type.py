from django.contrib import admin

from crm.models import CRMTaskType
from utility.admin import BaseAdmin


@admin.register(CRMTaskType)
class CRMTaskTypeAdmin(BaseAdmin):

    list_display = [
        'id',
        'name',
        'title',
    ]