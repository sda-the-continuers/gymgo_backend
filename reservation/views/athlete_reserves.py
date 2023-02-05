import django_filters
from django.db.models import F, Value, DateTimeField, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from account.permission_classes import IsAthlete, CanModifyObject
from gym.enums import SCHEDULED_SESSION_STATE_CANCELLED
from reservation.enums import RESERVE_STATES, RESERVE_STATE_CANCELLED
from reservation.models import Reserve
from reservation.serializers import ReserveSerializer
from utility.django import InRangeHijackFilterGenerator


class AthleteReserveFilterSet(FilterSet):
    states = InRangeHijackFilterGenerator(django_filters.ChoiceFilter).in_filter(
        choices=RESERVE_STATES, lookup_expr='in', method='filter_states'
    )

    def filter_states(self, queryset, name, value):
        filter_ = Q(state__in=value)
        if RESERVE_STATE_CANCELLED in value:
            filter_ |= Q(scheduled_session__state=SCHEDULED_SESSION_STATE_CANCELLED)
        return queryset.filter(filter_)

    class Meta:
        model = Reserve
        fields = ['states']


class AthleteReserveView(ReadOnlyModelViewSet):
    queryset = Reserve.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete & CanModifyObject]
    serializer_class = ReserveSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering = ['till_now']
    filterset_class = AthleteReserveFilterSet

    def get_queryset(self):
        athlete = self.request.user.account.concrete_instance
        return super().get_queryset().filter(athlete=athlete).annotate(
            till_now=F('scheduled_session__start_datetime') - Value(timezone.now(), output_field=DateTimeField()),
        )
