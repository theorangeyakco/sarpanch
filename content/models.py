from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.utils import timezone, dateformat
from django.utils.text import slugify

from mptt.fields import TreeManyToManyField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from content.utils import validate_thumbnail_size, CreationModificationDateBase


class Category(MPTTModel, CreationModificationDateBase):
	parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
	                        related_name='children')
	title = models.CharField(max_length=200)

	class Meta:
		ordering = ["tree_id", "lft"]
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	class MPTTMeta:
		order_insertion_by = ["title"]

	def __str__(self):
		return self.title


class Post(models.Model):
	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'

	title = models.CharField(max_length=128)
	slug = models.SlugField(max_length=150)
	sub_title = models.CharField(max_length=512, help_text="A short description of the post")
	thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnails/', default='thumbnails/default.png',
	                              validators=[validate_thumbnail_size],
	                              help_text="Upload a 200x200 image less than 256kb.")
	content = RichTextUploadingField(config_name='full')
	categories = TreeManyToManyField(Category, related_name="category_posts")
	published = models.BooleanField(default=False)
	created_on = models.DateTimeField(default=timezone.now)
	updated_on = models.DateTimeField(default=timezone.now)

	def clean(self):
		if self.thumbnail:
			w, h = get_image_dimensions(self.thumbnail)
			if w != 200:
				raise ValidationError(f"The thumbnail is {w}px. Please make sure its 200x200.")
			if h != 200:
				raise ValidationError(f"The thumbnail is {h}px. Please make sure its 200x200.")
		super(Post, self).clean()

	def save(self, *args, **kwargs):
		self.updated_on = timezone.now()
		if not self.pk:
			self.slug = slugify(f"{self.title}-{dateformat.format(timezone.now(), 'Y-m-d-H-i-s')}")
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.title} - Post Id: {self.id}"
