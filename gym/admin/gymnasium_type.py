from django.contrib import admin
from django.contrib.admin import ModelAdmin

from gym.models import GymnasiumType


@admin.register(GymnasiumType)
class GymnasiumTypeAdmin(ModelAdmin):

    list_display = [
        'id',
        'title',
        'title_fa',
    ]

    fields = [
        'id',
        'title',
        'title_fa',
        'sport_types',
    ]

    readonly_fields = ['id']
