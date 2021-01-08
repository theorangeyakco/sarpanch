from random import random

from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .models.models import PhoneOTP
from .serializer import CreateUserSerializer, LoginSerializer, ChangePasswordSerializer
from .utils import send_otp, password_valid

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class ValidatePhoneAndSendOTP(APIView):
	@staticmethod
	def post(request, *args, **kwargs):
		phone_number = request.data.get('phone_number')
		if phone_number:
			phone = str(phone_number)
			user = User.objects.filter(phone__iexact=phone)
			if user.exists():
				return Response({
					'status': False,
					'detail': 'User already exists.'
				})
			else:
				key = send_otp(phone)
				if key:
					old = PhoneOTP.objects.filter(phone__iexact=phone)
					if old.exists():
						old = old.first()
						count = old.count
						if count > 10:
							return Response({
								'status': False,
								'detail': 'OTP sending error. OTP limit reached. Please contact customer support.'
							})
						print("Count increased ", count)
						old.count += 1
						old.save()
						return Response({
							'status': True,
							'detail': 'Otp sent successfully'
						})
					else:
						PhoneOTP.objects.create(phone=phone, otp=key)
						return Response({
							'status': True,
							'detail': 'Otp sent successfully'
						})
				else:
					return Response({
						'status': False,
						'detail': 'Error in sending OTP'
					})
		else:
			return Response({
				'status': False,
				'detail': 'Phone number has not been provided.'
			})


class ValidateOTP(APIView):
	"""
	If the user has already received the OTP then this requests validates that OTP
	against the phone number provided, and allows the user to proceed to registration.
	"""

	@staticmethod
	def post(request, *args, **kwargs):
		phone = request.data.get('phone_number', False)
		otp_sent = request.data.get('otp', False)
		if (type(phone) == str) and (type(otp_sent) == str):
			old = PhoneOTP.objects.filter(phone__iexact=phone)
			if old.exists():
				old = old.first()
				otp = old.otp
				if str(otp_sent) == str(otp):
					old.validated = True
					old.save()
					return Response({
						'status': True,
						'detail': 'OTP validated. Please proceed to registration.'
					})
				else:
					return Response({
						'status': False,
						'detail': 'The OTP entered is incorrect'
					})
			else:
				return Response({
					'status': False,
					'detail': 'Phone number does not exist. Please send the otp first.'
				})
		else:
			return Response({
				'status': False,
				'detail': 'Please enter both the phone and the OTP for validation.'
			})


class Register(APIView):
	@staticmethod
	def post(request, *args, **kwargs):
		phone = request.data.get('phone_number', False)
		password = request.data.get('password', False)
		email = request.data.get('email', False)
		name = request.data.get('name')
		# REVIEW: What are the other fields that we want to get during
		#  registration

		if (type(phone) == str and type(password) == str and type(name) == str and type(email) == str):
			old = PhoneOTP.objects.filter(phone__iexact=phone)
			if old.exists():
				old = old.first()
				if old.validated:
					if password_valid(password):
						temp_data = {
							'phone'   : phone,
							'password': password,
							'name'    : name,
							'email'   : email
						}
						serializer = CreateUserSerializer(data=temp_data)
						serializer.is_valid(raise_exception=True)
						user = serializer.save()
						old.delete()
						return Response({
							'status': True,
							'detail': 'Account created'
						})
					else:
						return Response({
							'status': False,
							'detail': 'Invalid password: Password should have at least one digit, one uppercase and one'
							          ' lowercase character, one special character, and should be 6 to 20 characters long'
						})
				else:
					return Response({
						'status': False,
						'detail': 'Please verify your OTP before registration.'
					})
			else:
				return Response({
					'status': False,
					'detail': 'Please request a OTP before registration.'
				})
		else:
			return Response({
				'status': False,
				'detail': 'Please enter both the phone number and the password'
			})


class Login(KnoxLoginView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		if user.last_login is None:
			user.first_login = True
			user.save()

		elif user.first_login:
			user.first_login = False
			user.save()

		login(request, user)
		return super(Login, self).post(request, format=None)


class ChangePassword(generics.UpdateAPIView):
	"""
	Change password endpoint view
	"""
	authentication_classes = (TokenAuthentication,)
	serializer_class = ChangePasswordSerializer
	permission_classes = [permissions.IsAuthenticated, ]

	def get_object(self, queryset=None):
		"""
		Returns current logged in user instance
		"""
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			if not self.object.check_password(serializer.data.get('password_1')):
				return Response({
					'status'          : False,
					'current_password': 'The current password does not match your password.',
				}, status=status.HTTP_400_BAD_REQUEST)

			if not password_valid(serializer.data.get('password_2')):
				return Response({
					'status': False,
					'detail': 'Invalid password: Password should have at least one digit, one uppercase and one'
					          ' lowercase character, one special character, and should be 6 to 20 characters long'
				})

			self.object.set_password(serializer.data.get('password_2'))
			self.object.password_changed = True
			self.object.save()
			return Response({
				"status": True,
				"detail": "Password has been successfully changed.",
			})

		return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
