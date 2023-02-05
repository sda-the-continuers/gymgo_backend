from django.contrib import admin

from reservation.models import Reserve


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    pass
