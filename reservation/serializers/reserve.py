from jalali_date import datetime2jalali
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import GymUsage, ScheduledSession
from reservation.models import Reserve


class ScheduledSessionForReserveSerializer(ModelSerializer):
    state_fa = serializers.CharField(source='get_state_display', read_only=True)
    jalali_start_datetime = serializers.DateTimeField()
    jalali_end_datetime = serializers.DateTimeField()

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
        ]


class GymUsageForReserveSerializer(ModelSerializer):
    sport_type = serializers.CharField(source='type.title')
    sport_type_fa = serializers.CharField(source='type.title_fa')
    gymnasium_type = serializers.CharField(source='gymnasium.type.title')
    gymnasium_type_fa = serializers.CharField(source='gymnasium.type.title_fa')
    address = serializers.CharField(source='gymnasium.gym_complex.address')

    class Meta:
        model = GymUsage
        fields = [
            'id',
            'sport_type',
            'sport_type_fa',
            'gymnasium_type',
            'gymnasium_type_fa',
            'address',
        ]


class ReserveSerializer(ModelSerializer):
    gym_usage = GymUsageForReserveSerializer(read_only=True)
    scheduled_session = ScheduledSessionForReserveSerializer(read_only=True)
    state_fa = serializers.CharField(source='get_state_display', read_only=True)
    paid_price = serializers.CharField(source='paid_price_from_athlete', read_only=True)

    class Meta:
        model = Reserve
        fields = [
            'id',
            'scheduled_session',
            'gym_usage',
            'athlete',
            'state',
            'state_fa',
            'paid_price',
        ]
