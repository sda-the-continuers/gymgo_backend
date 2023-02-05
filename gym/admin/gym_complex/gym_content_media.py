from django.contrib import admin
from nested_admin.nested import NestedStackedInline

from gym.models import GymContentMedia, GymContentMediaBase, GymThumbnail, GymContentMediaInterface
from utility.admin.utility_link_admin import UtilityLinkAdmin


class GymContentMediaBaseInline(UtilityLinkAdmin, NestedStackedInline):
    model = None
    extra = 1

    fields = [
        'file',
        'get_file',
    ]

    readonly_fields = ['get_file']

    def get_file(self, instance: GymContentMediaBase):
        return self.get_image_html(instance.file.url)


class GymContentMediaInline(GymContentMediaBaseInline):
    model = GymContentMedia


class GymThumbnailInline(GymContentMediaBaseInline):
    model = GymThumbnail


@admin.register(GymContentMediaInterface)
class GymContentMediaInterfaceAdmin(admin.ModelAdmin):
    inlines = [
        GymThumbnailInline,
        GymContentMediaInline,
    ]
    list_display = [
        'id'
    ]
    fields = [
        'id'
    ]
    readonly_fields = [
        'id'
    ]
