from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import RadioSelect

from ..models import User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


GENDER_CHOICES = [
	(None, ''),          # show blank by default
	('M', 'Male'),
	('F', 'Female'),
	('T', 'Transgender'),
	('O', 'Other'),
	('N', 'Prefer not say')
]


NOTIFICATION_LEVEL_CHOICES = [
	(0, 'Disable All Notifications'),
	(1, 'Email me only when its critical'),
	(2, 'Email me reminders and updates'),
	(3, 'Email me some promotions'),
	(4, 'Keep all notifications on')
]


class EditProfileForm(forms.Form):
	name = forms.CharField(label='Full name', required=True)
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES,
	                           required=False)
	avatar = forms.ImageField(label='Profile Picture',
	                          required=False)
	email = forms.EmailField(label='Email', required=False)


class UpdateNotification(forms.Form):
	notification_level = forms.ChoiceField(label='Notification Level',
	                                       choices=NOTIFICATION_LEVEL_CHOICES,
	                                       widget=RadioSelect,
	                                       required=False)
