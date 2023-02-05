from django.contrib import admin

from crm.models import CRMTask
from utility.admin import BaseAdmin


@admin.register(CRMTask)
class CRMTaskAdmin(BaseAdmin):

    list_display = [
        'id',
        'get_task_type',
        'get_customer',
        'description',
        'state'
    ]

    @admin.display(description='نوع تسک')
    def get_task_type(self, obj):
        return self.link_display_style_detailed(obj.task_type, 'name')

    @admin.display(description='مشتری')
    def get_customer(self, obj):
        return self.link_display_style_raw(obj.customer)