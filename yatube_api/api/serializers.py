from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='post.pk'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
