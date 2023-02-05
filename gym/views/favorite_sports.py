from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from account.permission_classes import IsAthlete
from gym.models import SportType
from gym.serializers import FavoriteSportsSerializer, SelectFavoriteSportsSerializer


class FavoriteSportsView(
    UpdateModelMixin, ListModelMixin, GenericViewSet
):
    queryset = SportType.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SelectFavoriteSportsSerializer
        return FavoriteSportsSerializer

    def get_object(self):
        if self.action == 'partial_update':
            return self.request.user.account.concrete_instance
        return super().get_object()
