from random import randint

from requests import get


def otp_generator():
	otp = randint(999, 9999)
	return otp


def send_otp(phone):
	"""
	This is an helper function to send otp to session stored phones or
	passed phone number as argument.
	"""
	SENDER_ID = "SRPNCH"
	API_KEY = ""
	TEMPLATE_NAME = "OTP%20Validation"

	if phone:

		key = otp_generator()
		phone = str(phone)
		otp_key = str(key)
		name = "user"

		link = f"https://2factor.in/API/R1/?" \
		       f"module=TRANS_SMS" \
		       f"&apikey={API_KEY}&" \
		       f"to={phone}&" \
		       f"from={SENDER_ID}&" \
		       f"templatename={TEMPLATE_NAME}&" \
		       f"var1={name}&" \
		       f"var2={otp_key}"

		# result = get(link, verify=False)

		return otp_key
	else:
		return False
