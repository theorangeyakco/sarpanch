import re
from os import getenv
from random import randint

from requests import get
from rest_framework.generics import get_object_or_404

from accounts.models import User


def otp_generator() -> str:
	otp = randint(999, 9999)
	return str(otp)


def _send_otp(phone, forgot=False):
	"""
	This is an helper function to send otp to session stored phones or
	passed phone number as argument.
	"""
	SENDER_ID = "SRPNCH"
	API_KEY = getenv("SMS_API_KEY")
	TEMPLATE_NAME = "OTP%20Validation"  # needs to be url friendly

	if phone:

		otp_key = otp_generator()
		phone = str(phone)
		if not forgot:
			name = "user"
		else:
			user = get_object_or_404(User, phone__iexact=phone)
			if user.name:
				name = user.name
			else:
				name = user.phone
		link = f"https://2factor.in/API/R1/?" \
		       f"module=TRANS_SMS" \
		       f"&apikey={API_KEY}&" \
		       f"to={phone}&" \
		       f"from={SENDER_ID}&" \
		       f"templatename={TEMPLATE_NAME}&" \
		       f"var1={name}&" \
		       f"var2={otp_key}"

		response = get(link, verify=True)
		if 200 <= response.status_code < 300:
			return otp_key
		else:
			print(f"Error: 2factor.in returned status code {response.status_code}.", response)
			return False
	else:
		return False


def send_otp(phone):
	return _send_otp(phone)


def send_otp_forgot(phone):
	return _send_otp(phone, forgot=True)


def password_valid(password: str) -> bool:
	regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
	if re.search(regex, password):
		return True
	return False
