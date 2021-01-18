from rest_framework import serializers

from content.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'title', 'parent')


class PostSerializer(serializers.ModelSerializer):
	categories = CategorySerializer(many=True)

	class Meta:
		model = Post
		fields = ('id', 'title', 'sub_title', 'slug', 'thumbnail', 'content',
		          'created_on', 'updated_on', 'categories')



