from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ValidatePhoneAndSendOTP, ValidateOTP
app_name = 'accounts'

urlpatterns = [
	path('validate_phone_and_send_otp/', csrf_exempt(ValidatePhoneAndSendOTP.as_view()), name='validate_phone_and_send_otp'),
	path('validate_otp/', csrf_exempt(ValidateOTP.as_view()), name='validate_otp')
]
