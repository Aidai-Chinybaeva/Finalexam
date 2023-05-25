from django.db.utils import IntegrityError
from rest_framework import serializers
from .models import Comment, Post, PostMark



class PostSerializer(serializers.ModelSerializer):
    mark = serializers.ReadOnlyField(source='avg_mark')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', ]


class MarkPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostMark
        fields = "__all__"
        read_only_fields = ['user', 'post', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            mark = PostMark.objects.get(
                user=validated_data['user'],
                post_id=validated_data['post_id']
            )
            if mark.mark != validated_data['mark']:
                mark.mark = validated_data['mark']
                mark.save()
            return mark
