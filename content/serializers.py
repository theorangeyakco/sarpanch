from rest_framework import serializers

from content.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'sub_title', 'slug', 'thumbnail', 'content',
		          'created_on', 'updated_on', 'categories')


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'title', 'parent')
