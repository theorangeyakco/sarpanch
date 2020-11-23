from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .mixins import UserData


class UserManager(BaseUserManager):
	def _create_user(self, phone, password, username, **extra, ):
		if not phone:
			raise ValueError('Phone number must be set!')

		if not password:
			raise ValueError('Password must be set!')
		if not username:
			raise ValueError('Username  must be set!')

		user = self.model(
				username=username,
				phone=phone,
				**extra
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, phone, password, username, **extra):
		extra.setdefault('is_staff', False)
		extra.setdefault('is_superuser', False)
		return self._create_user(
				phone, password, username, **extra
		)

	def create_staffuser(self, username, phone, password, **extra):
		extra['is_staff'] = True
		extra['is_superuser'] = False
		return self._create_user(
				phone, password, username, **extra
		)

	def create_superuser(self, username, phone, password, **extra):
		extra['is_staff'] = True
		extra['is_superuser'] = True
		return self._create_user(
				phone, password, username, **extra
		)


class User(AbstractBaseUser, PermissionsMixin, UserData):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
	                             message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")

	phone = models.CharField(validators=[phone_regex], max_length=17, primary_key=True)
	username = models.CharField(max_length=32, unique=True)
	# password field supplied by AbstractBaseUser
	# last_login field supplied by AbstractBaseUser

	# user data supplied by UserData mixin

	date_joined = models.DateTimeField('date joined', default=timezone.now)
	is_active = models.BooleanField(
			'active', default=True,
			help_text='Designates whether this user should be treated as active.',
	)
	is_staff = models.BooleanField(
			'staff status', default=False,
			help_text='Designates whether the user can log into this admin site.',
	)

	# is_superuser field provided by PermissionsMixin
	# groups field provided by PermissionsMixin
	# user_permissions field provided by PermissionsMixin

	objects = UserManager()

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['username', 'password']

	def get_full_name(self):
		if self.name:
			return self.name
		else:
			return self.phone

	def __str__(self):
		if self.name:
			return f'{self.name} <{self.phone}>'
		else:
			return f'<{self.phone}>'
