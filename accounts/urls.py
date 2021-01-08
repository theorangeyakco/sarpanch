from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ValidatePhoneAndSendOTP, ValidateOTP, Register, Login, ChangePassword, ValidatePhoneForgot,\
	ForgotValidateOTP, ForgetPasswordChange
from knox import views as knox_views

app_name = 'accounts'

urlpatterns = [
	path('validate_phone_and_send_otp/', csrf_exempt(ValidatePhoneAndSendOTP.as_view()), name='validate_phone_and_send_otp'),
	path('validate_otp/', csrf_exempt(ValidateOTP.as_view()), name='validate_otp'),
	path('register/', csrf_exempt(Register.as_view()), name='register'),
	path('login/', csrf_exempt(Login.as_view()), name='login'),
	path('logout/', csrf_exempt(knox_views.LogoutView.as_view()), name='logout'),
	path('change_password/', csrf_exempt(ChangePassword.as_view()), name='change_password'),
	path('validate_phone_and_send_forgot_otp/', csrf_exempt(ValidatePhoneForgot.as_view()), name='validate_phone_and_send_forgot_otp'),
	path('validate_forgot_otp/', csrf_exempt(ForgotValidateOTP.as_view()), name='validate_forgot_otp'),
	path('change_forgotten_password/', csrf_exempt(ForgetPasswordChange.as_view()), name='change_forgotten_password'),

]
