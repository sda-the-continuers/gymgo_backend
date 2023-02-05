from django.db.models import OuterRef
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from account.permission_classes import IsAthlete
from gym.enums import SCHEDULED_SESSION_STATE_CANCELLED
from gym.models import GymUsage, ScheduledSession
from gym.serializers import GymUsageSerializer
from utility.django import MinSubquery


class GymUsageView(RetrieveModelMixin, GenericViewSet):
    queryset = GymUsage.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete]
    serializer_class = GymUsageSerializer

    def get_queryset(self):
        return super().get_queryset().annotate(
            session_minimum_price=MinSubquery(
                ScheduledSession.objects.exclude(state=SCHEDULED_SESSION_STATE_CANCELLED).filter(
                    gymnasium_id=OuterRef('gymnasium_id')
                ), min_field='price'
            )
        )
