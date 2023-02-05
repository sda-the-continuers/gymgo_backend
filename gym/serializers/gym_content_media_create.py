from rest_framework.serializers import ModelSerializer

from gym.models import GymContentMedia, GymThumbnail


class GymContentMediaCreateBase(ModelSerializer):
    class Meta:
        fields = [
            'file',
            'attachments_interface',
        ]


class GymContentMediaCreate(GymContentMediaCreateBase):
    class Meta:
        model = GymContentMedia
        fields = GymContentMediaCreateBase.Meta.fields


class GymThumbnailCreate(GymContentMediaCreateBase):
    class Meta:
        model = GymThumbnail
        fields = GymContentMediaCreateBase.Meta.fields
