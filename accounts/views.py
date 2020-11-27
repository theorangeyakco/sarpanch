from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User


class ValidatePhoneSendOTP(APIView):
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
			return Response({
				'status': False,
				'detail': 'Phone number has not been provided.'
			})
