from django.contrib import admin

from content.models import Post, Category
from django_mptt_admin.admin import DjangoMpttAdmin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'sub_title', 'published', 'created_on', 'updated_on')
	list_filter = ('categories',)
	filter_horizontal = ('categories',)
	readonly_fields = ('slug', 'created_on', 'updated_on')


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
	list_display = ["title", "created", "modified"]
	list_filter = ["created"]
