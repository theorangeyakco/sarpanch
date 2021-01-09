from django.db import models

from django.core.exceptions import ValidationError


def validate_thumbnail_size(field_file_obj):
	file_size = field_file_obj.file.size
	kilobyte_limit = 256
	if file_size >= kilobyte_limit * 1024:
		raise ValidationError(f"This image is {file_size / 1024}kb. Please make sure it is less than 256kb.")


class CreationModificationDateBase(models.Model):
	"""
	Abstract base class with a creation and modification date and time
	"""

	created = models.DateTimeField(
			"Creation Date and Time",
			auto_now_add=True,
	)

	modified = models.DateTimeField(
			"Modification Date and Time",
			auto_now=True,
	)

	class Meta:
		abstract = True
