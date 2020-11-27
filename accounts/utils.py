from random import random
from requests import get


def otp_generator():
	otp = random.randint(999, 9999)
	return otp


def send_otp(phone):
	"""
	This is an helper function to send otp to session stored phones or
	passed phone number as argument.
	"""

	if phone:

		key = otp_generator()
		phone = str(phone)
		otp_key = str(key)

		link = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={api_key}to={phone}&from=srpnch&templatename={template_name}&var1={name}&var2={otp_key}"

		result = get(link, verify=False)

		return otp_key
	else:
		return False
