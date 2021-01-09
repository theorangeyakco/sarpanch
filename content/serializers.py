from rest_framework import serializers

from content.models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'sub_title', 'slug', 'thumbnail', 'content',
		          'created_on', 'updated_on')

