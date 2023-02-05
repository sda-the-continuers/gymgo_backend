from django.db import transaction
from rest_framework.serializers import ModelSerializer

from gym.models import Gymnasium, GymUsage
from gym.serializers import ScheduledSessionSerializer, GymUsageEquipmentSerializer
from gym.serializers.mixins import ThumbnailContentMediaDeserializerMixin
from utility.drf.exceptions import type_safe_exception_wrapper
from utility.drf.serializers import CreateForRelatedMixin


class GymUsageCreateSerializer(CreateForRelatedMixin, ModelSerializer):
    equipments = GymUsageEquipmentSerializer(many=True, required=False)

    def to_internal_value(self, data):
        from gym.models import SportType
        if isinstance(data['type'], SportType):
            data['type'] = data['type'].id
        return super().to_internal_value(data)

    def create_for_related(self, gym_usage, serializer_class, data):
        return super().create_for_related('gym_usage', gym_usage, serializer_class, data)

    @type_safe_exception_wrapper
    def create(self, validated_data):
        with transaction.atomic():
            equipments_data = validated_data.pop('equipments', [])

            gym_usage: GymUsage = super().create(validated_data)
            self.create_for_related(gym_usage, GymUsageEquipmentSerializer, equipments_data)
            return gym_usage

    class Meta:
        model = GymUsage
        fields = [
            'type',
            'equipments',
        ]


class GymnasiumCreateSerializer(CreateForRelatedMixin, ThumbnailContentMediaDeserializerMixin, ModelSerializer):
    gym_usages = GymUsageCreateSerializer(many=True)
    scheduled_sessions = ScheduledSessionSerializer(many=True, required=False)

    def create_for_related(self, gymnasium, serializer_class, data):
        return super().create_for_related('gymnasium', gymnasium, serializer_class, data)

    def to_internal_value(self, data):
        from gym.models import GymnasiumType, GymnasiumAttribute
        if isinstance(data['type'], GymnasiumType):
            data['type'] = data['type'].id
        raw_attributes = []
        for attribute in data['attributes']:
            if isinstance(attribute, GymnasiumAttribute):
                raw_attributes.append(attribute.id)
        data['attributes'] = raw_attributes or data['attributes']
        return super().to_internal_value(data)

    def create(self, validated_data):
        with transaction.atomic():
            gym_usages_data = validated_data.pop('gym_usages')
            scheduled_sessions_data = validated_data.pop('scheduled_sessions', [])
            media_data = validated_data.pop('set_media', [])
            thumbnail_data = validated_data.pop('set_thumbnail', None)

            gymnasium: Gymnasium = super().create(validated_data)
            self.create_for_related(
                gymnasium, GymUsageCreateSerializer, gym_usages_data
            )
            self.create_for_related(
                gymnasium, ScheduledSessionSerializer, scheduled_sessions_data
            )
            from gym.models import GymContentMedia, GymThumbnail
            GymContentMedia.objects.filter(id__in=media_data).update(
                attachments_interface=gymnasium.attachments_interface_id
            )
            GymThumbnail.objects.filter(id=thumbnail_data).update(
                attachments_interface=gymnasium.attachments_interface_id
            )
            return gymnasium

    class Meta:
        model = Gymnasium
        fields = [
            'type',
            'description',
            'price',
            'gym_owner_price',
            'rules',
            'length',
            'width',
            'attributes',
            'scheduled_sessions',
            'gym_usages',
            *ThumbnailContentMediaDeserializerMixin.Meta.fields,
        ]
