from django_admin_inline_paginator.admin import PaginationFormSetBase, TabularInlinePaginated


class PaginationFormSetBaseWithName(PaginationFormSetBase):
    def get_page_num(self) -> int:
        page = self.request.GET.get(self.page_name, '1')
        if page.isnumeric() and page > '0':
            return int(page)

        return 1

    def other_params(self):
        query_string = (self.request.META.get('QUERY_STRING') or '')
        if self.page_name not in self.request.GET:
            return query_string + '&'
        page = self.request.GET.get(self.page_name)
        query_string.replace('&{}={}'.format(self.page_name, page), '')
        query_string.replace('{}={}'.format(self.page_name, page), '')
        return query_string + '&'

    def __init__(self, *args, **kwargs):
        self.page_name = kwargs['prefix']
        super().__init__(*args, **kwargs)


class TabularInlinePaginatedWithName(TabularInlinePaginated):
    pagination_formset_class = PaginationFormSetBaseWithName

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super().get_formset(request, obj, **kwargs)

        class PaginationFormSet(PaginationFormSetBaseWithName, formset_class):
            pass

        PaginationFormSet.request = request
        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet
