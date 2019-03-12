from rest_framework import serializers
from .models import Profile, Post, Like, Comment


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    friends = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='friend-detail'
    )

    friends_requests = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='friend-request-detail'
    )

    username = serializers.ReadOnlyField(source='__unicode__')

    class Meta:
        model = Profile
        fields = ('username', 'friends', 'friends_requests', 'age', 'sex',
                    'bio', 'picture', 'picture_thumbnail', 'created_at')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'text', 'picture', 'picture_standardized', 'created_at')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'created_at')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'text', 'created_at')