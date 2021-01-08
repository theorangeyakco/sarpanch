from random import random

from django.contrib.auth import login
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .models.models import PhoneOTP
from .serializer import CreateUserSerializer, LoginSerializer, ChangePasswordSerializer, ForgetPasswordSerializer
from .utils import send_otp, password_valid, send_otp_forgot

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


class ValidatePhoneForgot(APIView):
	"""
	Validate if account exists for a given phone number and then send otp for forgot password reset
	"""

	def post(self, request, *args, **kwargs):
		phone_number = request.data.get('phone')
		if phone_number:
			phone = str(phone_number)
			user = User.objects.filter(phone__iexact=phone)
			if user.exists():
				otp = send_otp_forgot(phone)
				print(phone, otp)
				if otp:
					otp = str(otp)
					count = 0
					old = PhoneOTP.objects.filter(phone__iexact=phone)
					if old.exists():
						old = old.first()
						k = old.count
						if k > 10:
							return Response({
								'status': False,
								'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
							})
						old.count = k + 1
						old.save()

						return Response({'status': True,
						                 'detail': 'OTP has been sent for password reset. Limits about to reach.'})

					else:
						count = count + 1

						PhoneOTP.objects.create(
								phone=phone,
								otp=otp,
								count=count,
								forgot=True,

						)
						return Response({'status': True, 'detail': 'OTP has been sent for password reset'})

				else:
					return Response({
						'status': 'False', 'detail': "OTP sending error. Please try after some time."
					})
			else:
				return Response({
					'status': False,
					'detail': 'Phone number not recognised. Kindly try a new account for this number'
				})


class ForgotValidateOTP(APIView):
	"""
	If you have received an otp, post a request with phone and that otp and you will be redirected to reset the forgotten password
	"""

	def post(self, request, *args, **kwargs):
		phone = request.data.get('phone', False)
		otp_sent = request.data.get('otp', False)

		if phone and otp_sent:
			old = PhoneOTP.objects.filter(phone__iexact=phone)
			if old.exists():
				old = old.first()
				if old.forgot == False:
					return Response({
						'status': False,
						'detail': 'Please get and otp to reset you password first.'
					})

				otp = old.otp
				if str(otp) == str(otp_sent):
					old.forgot_logged = True
					old.save()

					return Response({
						'status': True,
						'detail': 'OTP matched, please proceed to create new password'
					})
				else:
					return Response({
						'status': False,
						'detail': 'OTP incorrect, please try again'
					})
			else:
				return Response({
					'status': False,
					'detail': 'Phone not recognised. Please request a new otp with this number'
				})
		else:
			return Response({
				'status': 'False',
				'detail': 'Either phone or otp was not received in Post request'
			})


class ForgetPasswordChange(APIView):
	"""
	if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
	"""

	def post(self, request, *args, **kwargs):
		phone = request.data.get('phone', False)
		otp = request.data.get("otp", False)
		password = request.data.get('password', False)

		if phone and otp and password:
			old = PhoneOTP.objects.filter(Q(phone__iexact=phone) & Q(otp__iexact=otp))
			if old.exists():
				old = old.first()
				if old.forgot_logged:
					post_data = {
						'phone'   : phone,
						'password': password
					}
					user_obj = get_object_or_404(User, phone__iexact=phone)
					serializer = ForgetPasswordSerializer(data=post_data)
					serializer.is_valid(raise_exception=True)
					if user_obj:
						user_obj.set_password(serializer.data.get('password'))
						user_obj.active = True
						user_obj.save()
						old.delete()
						return Response({
							'status': True,
							'detail': 'Password changed successfully. Please Login'
						})
				else:
					return Response({
						'status': False,
						'detail': 'OTP Verification failed. Please try again in previous step'
					})
			else:
				return Response({
					'status': False,
					'detail': 'Phone and otp are do not match or a new phone has entered. Request a new otp in forgot password'
				})
		else:
			return Response({
				'status': False,
				'detail': 'Post request parameters missing.'
			})
