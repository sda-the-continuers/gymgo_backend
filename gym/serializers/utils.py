from typing import Type, TYPE_CHECKING

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from account.models import Athlete, ProfilePicture
from reservation.models import Comment

if TYPE_CHECKING:
    from gym.models import GymContentMediaBase


def generate_content_media_serializer(model_class: Type['GymContentMediaBase']):
    class GymContentMediaSerializer(ModelSerializer):
        class Meta:
            model = model_class
            fields = [
                'id',
                'file',
            ]

    return GymContentMediaSerializer


class AthleteInCommentInGymSerializer(ModelSerializer):
    class ProfilePictureSerializer(ModelSerializer):
        class Meta:
            model = ProfilePicture
            fields = [
                'id',
                'file',
            ]

    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, instance: Athlete):
        return self.ProfilePictureSerializer(
            instance.profile_picture,
            allow_null=True,
            context=self.context,
        ).data

    class Meta:
        model = Athlete
        fields = [
            'full_name',
            'profile_pic'
        ]


class CommentInGymSerializer(ModelSerializer):
    jalali_created = serializers.DateTimeField(read_only=True)
    athlete = AthleteInCommentInGymSerializer(source='reserve.athlete')

    class Meta:
        model = Comment
        fields = [
            'id',
            'score',
            'created',
            'jalali_created',
            'comment_text',
            'athlete',
        ]
