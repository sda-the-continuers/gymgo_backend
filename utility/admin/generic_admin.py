from django.contrib import admin


class GenericAdmin(admin.ModelAdmin):
    exclude = ['is_deleted']
    default_readnoly_fields = ['id', 'get_jalali_created', 'get_jalali_updated']

    # deletes XXX object (X) from title of a change view in django admin
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'subtitle': ''}
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        readonly_fields += GenericAdmin.default_readnoly_fields
        return readonly_fields

    def get_clean_fields(self, request, obj):
        fields = self.get_fields(request, obj)
        for readonly_field in self.default_readnoly_fields:
            if readonly_field in fields:
                fields.remove(readonly_field)
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = list()
        fieldsets.append(
            (
                None, {
                    'fields': [
                        *GenericAdmin.default_readnoly_fields
                    ]
                }
            ),
        )
        fieldsets.append(
            (
                'جزییات', {
                    'fields': [
                        *self.get_clean_fields(request, obj)
                    ]
                }
            )
        )
        return fieldsets
