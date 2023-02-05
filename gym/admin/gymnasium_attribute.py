from django.contrib import admin
from django.contrib.admin import ModelAdmin

from gym.models import GymnasiumAttribute


@admin.register(GymnasiumAttribute)
class GymnasiumAttributeAdmin(ModelAdmin):

    list_display = ['id', 'title', 'title_fa']

    fields = ['id', 'title', 'title_fa']

    readonly_fields = ['id']

