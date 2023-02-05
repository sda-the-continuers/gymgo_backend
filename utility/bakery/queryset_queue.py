from collections import Iterable

from django.db import transaction
from django.db.models import F, ExpressionWrapper, DurationField, Expression, Max, Value
from django.db.models.functions import Greatest, Coalesce
from django.utils import timezone

from utility.bakery import QueueInterface


class QuerysetQueue(QueueInterface):
    queryset = None
    order_by_field = 'created'
    latency_expression: Expression = F('updated')
    skip_locked = True
    zero_timedelta = Value(timezone.timedelta(seconds=0))

    @classmethod
    def order_queryset(cls, queryset):
        if isinstance(cls.order_by_field, str):
            return queryset.all().order_by(cls.order_by_field).all()
        elif isinstance(cls.order_by_field, Iterable):
            return queryset.all().order_by(*cls.order_by_field).all()
        else:
            return queryset.all().order_by(cls.order_by_field).all()

    @classmethod
    def get_ordered_queryset(cls):
        return cls.order_queryset(cls.get_queryset())

    @classmethod
    def get_locked_first(cls):
        return cls.get_ordered_queryset().select_for_update(skip_locked=cls.skip_locked).first()

    @classmethod
    def first(cls):
        return cls.get_ordered_queryset().first()

    @classmethod
    def count(cls):
        return cls.get_ordered_queryset().count()

    @classmethod
    def annotate_latency_field(cls, queryset, latency_field_name='latency'):
        return queryset.annotate(
            **{
                latency_field_name: ExpressionWrapper(
                    Greatest(timezone.now() - cls.latency_expression, cls.zero_timedelta),
                    output_field=DurationField(),
                ),
            }
        )

    @classmethod
    def latency(cls):
        return cls.annotate_latency_field(
            cls.get_ordered_queryset(),
            latency_field_name='latency',
        ).aggregate(latest=Coalesce(Max('latency'), cls.zero_timedelta))['latest']

    @classmethod
    def get_batch(cls, size):
        for i in range(size):
            first = cls.first()
            if first is None:
                break
            yield first

    @classmethod
    def run_locked_batch(cls, size, function_for_each=None, function_for_all=None):
        with transaction.atomic():
            objects = list(cls.get_ordered_queryset().select_for_update()[:size])
            if function_for_each is not None:
                for obj in objects:
                    function_for_each(obj)
            if function_for_all is not None:
                function_for_all(objects)

    @classmethod
    def get_queryset(cls):
        if cls.queryset is None:
            raise Exception('You have to either set queryset field or override get_queryset method.')
        return cls.queryset
