from rest_framework import mixins
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from account.models import Athlete, GymOwner, ProfilePicture
from account.permission_classes import IsGymOwner, IsAthlete
from account.serializers import AthleteProfileSerializer
from account.serializers.profile import GymOwnerProfileSerializer, ProfilePictureSerializer


class AthleteProfileView(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    serializer_class = AthleteProfileSerializer
    queryset = Athlete.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete]

    def get_object(self):
        return self.request.user.account.concrete_instance


class GymOwnerProfileView(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    serializer_class = GymOwnerProfileSerializer
    queryset = GymOwner.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGymOwner]

    def get_object(self):
        return self.request.user.account.concrete_instance


class ProfilePictureView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = ProfilePictureSerializer
    queryset = ProfilePicture.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAthlete]

    def get_queryset(self):
        return super().get_queryset().filter(
            account_id=self.request.user.account.id,
            is_active=True,
        )
