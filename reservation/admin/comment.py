from django.contrib import admin

from reservation.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
