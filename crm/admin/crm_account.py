from django.contrib import admin

from crm.models import CRMAccount


@admin.register(CRMAccount)
class CRMAccountAdmin(admin.ModelAdmin):
    pass
