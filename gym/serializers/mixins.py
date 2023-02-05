from abc import abstractmethod
from functools import lru_cache
from typing import TYPE_CHECKING, Union

from django.db.models import Avg, Count, QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from gym.models import GymThumbnail, GymContentMedia
from gym.serializers.utils import generate_content_media_serializer, CommentInGymSerializer

if TYPE_CHECKING:
    from gym.models import GymComplex, Gymnasium, GymUsage


class CommentSerializerBase(ModelSerializer):

    @lru_cache()
    def get_instance_comments(self, instance: Union['GymComplex', 'Gymnasium', 'GymUsage']):
        from reservation.models import Comment
        return Comment.get_comments_for_gym(
            instance
        )


class AthleteReviewsSerializerMixin(CommentSerializerBase):
    athlete_reviews = serializers.SerializerMethodField()

    def get_athlete_reviews(self, instance: Union['GymComplex', 'Gymnasium', 'GymUsage']):
        return self.get_instance_comments(instance).aggregate(
            average_score=Avg('score'),
            reviews_count=Count('*'),
        )

    class Meta:
        fields = [
            'athlete_reviews'
        ]


class CommentsSerializerMixin(CommentSerializerBase):
    comments = serializers.SerializerMethodField()

    def get_comments(self, instance: Union['GymComplex', 'Gymnasium', 'GymUsage']):
        return CommentInGymSerializer(
            self.get_instance_comments(instance),
            many=True,
            allow_null=True,
            context=self.context,
        ).data

    class Meta:
        fields = [
            'comments'
        ]


class ThumbnailContentMediaSerializerMixin(ModelSerializer):
    thumbnail = generate_content_media_serializer(GymThumbnail)(
        source='attachments_interface.thumbnail', allow_null=True
    )
    media = serializers.SerializerMethodField()

    @abstractmethod
    def get_content_media_for_serializing(self, instance) -> QuerySet:
        pass

    def get_media(self, instance):
        qs = self.get_content_media_for_serializing(instance)
        serializer = generate_content_media_serializer(GymContentMedia)(
            qs,
            many=True,
            allow_null=True,
            context=self.context,
        )
        return serializer.data

    class Meta:
        fields = [
            'thumbnail',
            'media',
        ]


class ThumbnailContentMediaDeserializerMixin(ModelSerializer):
    set_media = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    set_thumbnail = serializers.IntegerField(write_only=True, required=False)

    def validate_set_media(self, value):
        from gym.models import GymContentMedia
        if GymContentMedia.objects.exclude(
                attachments_interface__isnull=False
        ).filter(id__in=value).count() != len(value):
            raise ValidationError({
                'media': ['عکس‌های ارسالی معتبر نیستند!']
            })
        return value

    def validate_set_thumbnail(self, value):
        from gym.models import GymThumbnail
        if not GymThumbnail.objects.exclude(
                attachments_interface__isnull=False
        ).filter(id=value).exists():
            raise ValidationError({
                'thumbnail': ['عکس thumbnail ارسالی معتبر نیست!']
            })
        return value

    class Meta:
        fields = [
            'set_media',
            'set_thumbnail',
        ]
