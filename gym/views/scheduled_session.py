import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings

from account.permission_classes import IsAthlete
from gym.models import ScheduledSession, GymUsage
from gym.serializers import ScheduledSessionSerializer


class ScheduledSessionFilterSet(FilterSet):
    gym_usage = django_filters.ModelChoiceFilter(
        queryset=GymUsage.objects.all(), to_field_name='id', method='filter_gym_usage'
    )

    def filter_gym_usage(self, queryset, name, value: GymUsage):
        if 'gymnasium' in self.data:
            return queryset
        return queryset.filter(gymnasium_id=value.gymnasium_id)

    class Meta:
        model = ScheduledSession
        fields = {
            'gymnasium': ['exact'],
            'start_datetime': ['gt', 'lt', 'gte', 'lte'],
            'end_datetime': ['gt', 'lt', 'gte', 'lte'],
        }


class ScheduledSessionView(ListAPIView):
    queryset = ScheduledSession.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete]
    serializer_class = ScheduledSessionSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = ScheduledSessionFilterSet
    ordering = ['start_datetime']

