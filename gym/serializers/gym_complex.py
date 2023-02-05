from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import GymComplex, Gymnasium, GymUsage, SportType
from gym.serializers.mixins import AthleteReviewsSerializerMixin, ThumbnailContentMediaSerializerMixin


class SportTypeInGymUsageSerializer(ModelSerializer):

    class Meta:
        model = SportType
        fields = ['id', 'title', 'title_fa', 'icon']


class GymUsageInGymnasiumSerializer(ModelSerializer):
    type = SportTypeInGymUsageSerializer()

    class Meta:
        model = GymUsage
        fields = [
            'id',
            'type',
        ]


class GymnasiumInGymComplexSerializer(ModelSerializer):
    gymnasium_type = serializers.CharField(source='type.title')
    gymnasium_type_fa = serializers.CharField(source='type.title_fa')
    gym_usages = GymUsageInGymnasiumSerializer(many=True, source='active_gym_usages')

    class Meta:
        model = Gymnasium
        fields = [
            'id',
            'gymnasium_type',
            'gymnasium_type_fa',
            'gym_usages',
        ]


class GymComplexSerializer(ThumbnailContentMediaSerializerMixin, AthleteReviewsSerializerMixin, ModelSerializer):
    gymnasiums = GymnasiumInGymComplexSerializer(many=True, read_only=True, source='active_gymnasiums')

    def get_content_media_for_serializing(self, instance: GymComplex) -> QuerySet:
        from gym.models import GymContentMedia
        return GymContentMedia.objects.filter(attachments_interface_id__in=[
            instance.attachments_interface_id,
            *list(gymnasium.attachments_interface_id for gymnasium in instance.active_gymnasiums)
        ])

    class Meta:
        model = GymComplex
        fields = [
            'id',
            'club',
            'code',
            'phone_number',
            'name',
            'owner',
            'address',
            'description',
            'rules',
            'instagram_username',
            'gymnasiums',
            *AthleteReviewsSerializerMixin.Meta.fields,
            *ThumbnailContentMediaSerializerMixin.Meta.fields,
        ]
