from django.contrib import admin

from crm.models import TicketType
from utility.admin import BaseAdmin


@admin.register(TicketType)
class TicketTypeAdmin(BaseAdmin):

    list_display = [
        'id',
        'title',
        'title_fa',
        'priority'
    ]