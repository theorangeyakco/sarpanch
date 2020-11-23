from django.contrib.auth.forms import UserCreationForm
from django import forms
from ..models import User


class RegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', required=True)
	email = forms.EmailField(label='Email ID', required=True)
	name = forms.CharField(label='Full name', required=True)
	phone = forms.CharField(label='Mobile Number', required=True)
	password = forms.PasswordInput()

	class Meta:
		model = User
		fields = (
			'username', 'name', 'email', 'phone', 'password1', 'password2'
		)

	def save(self, commit=True):
		user = super(self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user
