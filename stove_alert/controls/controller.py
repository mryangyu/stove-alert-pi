import time
import datetime
import sensors
import electronics

from termcolor import colored
from utils.patterns import *
from twilio.rest import TwilioRestClient

class Twilio(Serializable):
	# Your Account Sid and Auth Token from twilio.com/user/account
	def __init__(self):
		account_sid = "AC34e58ff24ae02348b2250f766f361139"
		auth_token  = "b0f58333f7dea30be9df8624f2450e4e"
		
		self.client = TwilioRestClient(account_sid, auth_token)

	def sms(self, to, body):
		message = self.client.messages.create(body=body, to=to, from_=MOCKED['system'])
		return message.sid

twilio = Twilio()

MOCKED = {
		'system': "+16475608477",
		"triggers": ['+16473009264', "+15145601025"]
	}

@Singleton
class Controller(Serializable):
	_last_alert_at = None
	def __init__(self):
		self._level = 0
		self.sensors = sensors.Sensors()
		self.ui = sensors.UI()
		self._last_temeprature = None

	def sms_user(self):
		twilio.sms(MOCKED['triggers'][self._level], "Fire!!! Fire!!!!!")

	@electronics.digestion
	def preventation(self):
		if not self.ui.power: return
		if self._level > 0 and (Controller._last_alert_at - datetime.datetime.now()).total_seconds < 10: return

		if self.sensors.temperature > 40:
			if not self.ui.buzzer: self.ui.buzzer = True

			self._last_temeprature = self.sensors.temperature
			Controller._last_alert_at = datetime.datetime.now()

			if self._level < 3:
				self.sms_user()
			else:
				self.ui.power = False
			self._level += 1

		else:
			if self.ui.buzzer: self.ui.buzzer = False

	@electronics.digestion
	def commands(self, commands):
		for key in commands:
			if key == "buzzer":
				self.ui.buzzer = bool(commands[key])
			elif key == "power":
				self.ui.power = bool(commands[key])