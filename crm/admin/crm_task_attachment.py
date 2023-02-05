from django.contrib import admin

from crm.models import CRMTaskAttachment
from utility.admin import BaseAdmin


@admin.register(CRMTaskAttachment)
class CRMTaskAttachmentAdmin(BaseAdmin):

    list_display = [
        'id',
        'get_crm_task',
        'file'
    ]

    @admin.display(description='تسک crm')
    def get_crm_task(self, obj):
        return self.link_display_style_raw(obj.crm_task)
