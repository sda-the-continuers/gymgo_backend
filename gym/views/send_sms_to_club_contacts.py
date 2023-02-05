from rest_framework.generics import CreateAPIView
from rest_framework.settings import api_settings

from account.permission_classes import IsGymOwner
from gym.models import ClubSMS, ClubSMSForDiscount
from gym.serializers import ClubSMSDeserializer, ClubSMSForDiscountDeserializer


class SendSMSToClubContactsView(CreateAPIView):
    queryset = ClubSMS.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGymOwner]
    serializer_class = ClubSMSDeserializer


class SendSMSForDiscountToClubContactsView(SendSMSToClubContactsView):
    queryset = ClubSMSForDiscount.objects.all()
    serializer_class = ClubSMSForDiscountDeserializer
