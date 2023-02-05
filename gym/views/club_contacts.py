from django.db.models import OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from account.permission_classes import IsGymOwner, CanModifyObject
from gym.models import ClubContact
from gym.serializers import ClubContactSerializer
from utility.django import CountSubquery


class ClubContactsView(ReadOnlyModelViewSet):
    queryset = ClubContact.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGymOwner & CanModifyObject]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['club__gym_complex', 'club']
    serializer_class = ClubContactSerializer

    def get_queryset(self):
        gym_owner = self.request.user.account.concrete_instance
        qs = super().get_queryset()
        from reservation.models import Reserve
        from reservation.enums import RESERVE_STATE_DONE
        return qs.filter(
            club__gym_complex__owner_id=gym_owner.id
        ).annotate(
            reserves_count=CountSubquery(
                Reserve.objects.filter(
                    athlete_id=OuterRef('athlete_id'),
                    scheduled_session__gymnasium__gym_complex_id=OuterRef('gym_complex_id'),
                    state=RESERVE_STATE_DONE,
                )
            )
        )
