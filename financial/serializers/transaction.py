from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from financial.models import Transaction


class TransactionSerializer(ModelSerializer):
    extra_info = serializers.SerializerMethodField()

    def get_extra_info(self, instance: Transaction):
        # TODO: get proper fields from transaction.parameters
        return {}

    class Meta:
        model = Transaction
        fields = [
            'wallet',
            'amount',
            'extra_info',
            'description',
            'jalali_created',
            'created',
        ]
