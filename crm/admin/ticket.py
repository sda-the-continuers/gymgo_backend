from django.contrib import admin

from crm.models import Ticket
from utility.admin import BaseAdmin


@admin.register(Ticket)
class TicketAdmin(BaseAdmin):

    list_display = [
        'id',
        'get_ticket_type',
        'get_customer',
        'state'
    ]

    @admin.display(description='نوع تیکت')
    def get_ticket_type(self, obj):
        return self.link_display_style_raw(obj.ticket_type)

    @admin.display(description='مشتری')
    def get_customer(self, obj):
        return self.link_display_style_raw(obj.customer)
