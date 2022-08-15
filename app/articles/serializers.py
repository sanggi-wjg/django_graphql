from rest_framework import serializers

from app.articles.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=1, max_length=250)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'datetime_created', 'datetime_updated')
