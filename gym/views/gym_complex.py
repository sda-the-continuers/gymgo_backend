from django.db.models import Prefetch
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from account.permission_classes import IsAthlete, IsGymOwner
from gym.models import GymComplex, Gymnasium, GymUsage
from gym.serializers import GymComplexSerializer, GymComplexCreateSerializer


class GymComplexBaseView(GenericViewSet):
    queryset = GymComplex.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES


class AthleteGymComplexView(RetrieveModelMixin, GymComplexBaseView):
    permission_classes = GymComplexBaseView.permission_classes + [IsAthlete]
    serializer_class = GymComplexSerializer
    lookup_field = 'code'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            qs = qs.prefetch_related(
                Prefetch(
                    'gymnasiums',
                    queryset=Gymnasium.objects.prefetch_related(
                        Prefetch(
                            'gym_usages',
                            queryset=GymUsage.objects.all(),
                            to_attr='active_gym_usages'
                        )
                    ),
                    to_attr='active_gymnasiums'
                ),
            )
        return qs


class GymOwnerGymComplex(CreateModelMixin, GymComplexBaseView):
    permission_classes = GymComplexBaseView.permission_classes + [IsGymOwner]
    serializer_class = GymComplexCreateSerializer

