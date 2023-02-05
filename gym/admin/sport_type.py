from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from gym.models import SportType, SportTypeIcon
from utility.admin.utility_link_admin import UtilityLinkAdmin


class SportTypeIconInline(UtilityLinkAdmin, TabularInline):
    model = SportTypeIcon
    extra = 1
    fields = [
        'file',
    ]

    def get_file(self, instance: SportTypeIcon):
        if instance.file:
            return self.get_image_html(instance.file.url, resize=False)
        return '---'


@admin.register(SportType)
class SportTypeAdmin(ModelAdmin):
    inlines = [
        SportTypeIconInline,
    ]

    list_display = [
        'id',
        'title',
        'title_fa',
    ]

    fields = [
        'id',
        'title',
        'title_fa',
    ]

    readonly_fields = ['id']

