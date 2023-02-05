from django.contrib import admin

from crm.models import TicketMessageAttachment
from utility.admin import BaseAdmin


@admin.register(TicketMessageAttachment)
class TicketMessageAttachmentAdmin(BaseAdmin):

    list_display = [
        'id',
        'get_ticket_message',
        'file'
    ]

    @admin.display(description='پیام تیکت')
    def get_ticket_message(self, obj):
        return self.link_display_style_raw(obj.ticket_message)