import time
import datetime
import sensors

from termcolor import colored
from utils.patterns import *
from twilio.rest import TwilioRestClient

MOCKED = {
		'system': "+16475608477",
		"yang": '+16473009264'
	}

@Singleton
class Controller(Serializable):
	def __init__(self):
		self.sensors = sensors.Sensors()
		self.ui = sensors.UI()
		self.twilio = Twilio()

	def initialize_components(self):
		self.sms_user()
		return

	def sms_user(self):
		self.twilio.sms(MOCKED['yang'], "Fire!!! Fire!!!!!")
 
class Twilio(Serializable):
	# Your Account Sid and Auth Token from twilio.com/user/account
	def __init__(self):
		account_sid = "AC34e58ff24ae02348b2250f766f361139"
		auth_token  = "b0f58333f7dea30be9df8624f2450e4e"
		
		self.client = TwilioRestClient(account_sid, auth_token)

	def sms(self, to, body):
		message = self.client.messages.create(body=body, to=to, from_=MOCKED['system'])
		return message.sid
