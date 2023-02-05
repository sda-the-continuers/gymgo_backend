from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import GymUsage, GymUsageEquipment
from gym.serializers import GymnasiumSerializer
from gym.serializers.mixins import AthleteReviewsSerializerMixin, CommentsSerializerMixin


class GymUsageEquipmentSerializer(ModelSerializer):
    class Meta:
        model = GymUsageEquipment
        fields = [
            'gym_usage',
            'type',
            'price',
        ]
        extra_kwargs = {
            'gym_usage': {
                'read_only': True,
            },
        }


class GymUsageSerializer(CommentsSerializerMixin, AthleteReviewsSerializerMixin, ModelSerializer):
    sport_type = serializers.CharField(source='type.title')
    sport_type_fa = serializers.CharField(source='type.title_fa')
    session_minimum_price = serializers.IntegerField(allow_null=True)
    gymnasium = GymnasiumSerializer(read_only=True)
    equipments = GymUsageEquipmentSerializer(many=True)

    class Meta:
        model = GymUsage
        annotated_fields = [
            'session_minimum_price',
        ]
        fields = [
            'id',
            'sport_type',
            'sport_type_fa',
            'gymnasium',
            'comments',
            'equipments',
            *annotated_fields,
            *AthleteReviewsSerializerMixin.Meta.fields,
            *CommentsSerializerMixin.Meta.fields,
        ]
