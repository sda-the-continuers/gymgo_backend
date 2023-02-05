from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from account.permission_classes import IsGymOwner
from financial.models import Transaction
from financial.serializers import TransactionSerializer


class TransactionsView(ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGymOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wallet', 'wallet__account']
    serializer_class = TransactionSerializer
