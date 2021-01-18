from abc import ABC

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('phone', 'password', 'name', 'email')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('phone', 'name', 'date_joined', 'email', 'is_active', 'avatar', 'last_login', 'first_login')


class LoginSerializer(serializers.Serializer):
	phone = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

	def validate(self, data):
		phone = data.get('phone')
		password = data.get('password')

		if phone and password:
			if User.objects.filter(phone=phone).exists():
				user = authenticate(request=self.context.get('request'), phone=phone, password=password)
			else:
				msg = {
					'status': False,
					'detail': 'This phone number does not exist. Please register first.'
				}
				raise serializers.ValidationError(msg)

			if not user:
				msg = {
					'status': False,
					'detail': 'Phone number and password do not match. Please try again.'
				}
				raise serializers.ValidationError(msg, code='authorization')
		else:
			msg = {
				'status': False,
				'detail': 'Please enter both phone and password.'
			}
			raise serializers.ValidationError(msg, code='authorization')

		data['user'] = user
		return data


class ChangePasswordSerializer(serializers.Serializer):
	"""
	Used for both password change (Login required) and
	password reset(No login required but otp required)
	not using modelserializer as this serializer will be used for for two apis
	"""

	password_1 = serializers.CharField(required=True)
	# password_1 can be old password or new password
	password_2 = serializers.CharField(required=True)
	# password_2 can be new password or confirm password according to apiview


class ForgetPasswordSerializer(serializers.Serializer):
	"""
	Used for resetting password who forget their password via otp verification
	"""
	phone = serializers.CharField(required=True)
	password = serializers.CharField(required=True)
