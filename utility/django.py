from typing import Type

import django_filters
from django.db import models
from django.db.models import Subquery


class CountSubquery(Subquery):
    template = "(SELECT COUNT(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


class SumSubquery(Subquery):
    template = "(SELECT SUM(%(sum_field)s) FROM (%(subquery)s) _sum)"
    output_field = models.IntegerField()

    def __init__(self, queryset, output_field=None, *, sum_field, **extra):
        extra['sum_field'] = sum_field
        queryset = queryset.values(sum_field)
        super().__init__(queryset, output_field, **extra)


class MinSubquery(Subquery):
    template = "(SELECT MIN(%(min_field)s) FROM (%(subquery)s) _min)"

    def __init__(self, queryset, output_field=None, *, min_field, **extra):
        extra['min_field'] = min_field
        super().__init__(queryset.values(min_field), output_field, **extra)


class MaxSubquery(Subquery):
    template = "(SELECT MAX(%(max_field)s) FROM (%(subquery)s) _max)"

    def __init__(self, queryset, output_field=None, *, max_field, **extra):
        extra['max_field'] = max_field
        super().__init__(queryset.values(max_field), output_field, **extra)


class StringAggSubquery(Subquery):
    template = "(SELECT STRING_AGG(%(string_field)s, %(delimiter)s) FROM (%(subquery)s) _string_agg)"
    output_field = models.CharField()

    def __init__(self, queryset, output_field=None, *, string_field, delimiter, **extra):
        extra['string_field'] = string_field
        extra['delimiter'] = f"'{delimiter}'"
        queryset = queryset.values(string_field)
        super().__init__(queryset, output_field, **extra)


class InRangeHijackFilterGenerator:
    IN_FILTER_INFIX = 'In'
    RANGE_FILTER_INFIX = 'Range'

    def __init__(self, base_type_filter: Type[django_filters.Filter]):
        self.base_type_filter = base_type_filter

    def get_filter_name(self, infix):
        return f'{self.base_type_filter.__name__.split("Filter")[0]}{infix}Filter'

    @property
    def in_filter(self):
        return type(
            self.get_filter_name(self.IN_FILTER_INFIX), (django_filters.BaseInFilter, self.base_type_filter), {}
        )

    @property
    def range_filter(self):
        return type(
            self.get_filter_name(self.RANGE_FILTER_INFIX), (django_filters.BaseRangeFilter, self.base_type_filter), {}
        )
