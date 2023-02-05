from django.contrib import admin

from crm.models import CustomerTicketMessage, ManagerTicketMessage


@admin.register(CustomerTicketMessage)
class CustomerTicketMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ManagerTicketMessage)
class ManagerTicketMessageAdmin(admin.ModelAdmin):
    pass
