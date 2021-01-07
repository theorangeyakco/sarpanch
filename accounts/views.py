from random import random

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .models.models import PhoneOTP
from .utils import send_otp


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
		# REVIEW: What are the other fields that we want to get during
		#  registration

		if phone and password:
			old = PhoneOTP.objects.filter(phone__iexact=phone)
			if old.exists():
				if old.validated:
					# TODO: Fill this in.
					pass
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
