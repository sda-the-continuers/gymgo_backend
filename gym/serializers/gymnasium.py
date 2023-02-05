from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import Gymnasium, GymnasiumAttribute
from gym.serializers.mixins import ThumbnailContentMediaSerializerMixin, CommentsSerializerMixin


class GymnasiumAttributeSerializer(ModelSerializer):
    class Meta:
        model = GymnasiumAttribute
        fields = [
            'title',
            'title_fa',
        ]


class GymnasiumSerializer(CommentsSerializerMixin, ThumbnailContentMediaSerializerMixin, ModelSerializer):
    gymnasium_type = serializers.CharField(source='type.title')
    gymnasium_type_fa = serializers.CharField(source='type.title_fa')
    attributes = GymnasiumAttributeSerializer(many=True)

    def get_content_media_for_serializing(self, instance: Gymnasium) -> QuerySet:
        from gym.models import GymContentMedia
        return GymContentMedia.objects.filter(attachments_interface_id=instance.attachments_interface.id)

    class Meta:
        model = Gymnasium
        fields = [
            'id',
            'gymnasium_type',
            'gymnasium_type_fa',
            'description',
            'rules',
            'comments',
            'attributes',
            *ThumbnailContentMediaSerializerMixin.Meta.fields,
            *CommentsSerializerMixin.Meta.fields,
        ]
