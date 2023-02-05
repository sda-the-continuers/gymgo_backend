from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import ScheduledSession


class ScheduledSessionSerializer(ModelSerializer):
    jalali_start_datetime = serializers.DateTimeField(read_only=True)
    jalali_end_datetime = serializers.DateTimeField(read_only=True)
    state_fa = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        model = ScheduledSession
        fields = [
            'id',
            'gymnasium',
            'start_datetime',
            'jalali_start_datetime',
            'end_datetime',
            'jalali_end_datetime',
            'state',
            'state_fa',
            'price',
        ]
        extra_kwargs = {
            'gymnasium': {
                'read_only': True,
            },
        }
