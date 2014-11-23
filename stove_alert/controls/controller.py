import time
import datetime
import sensors

from termcolor import colored
from utils.patterns import *


@Singleton
class Controller(Serializable):
	def __init__(self):
		self.sensors = sensors.Sensors()
		self.ui = sensors.UI()

	def initialize_components(self):
		return