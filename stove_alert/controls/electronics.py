import types
import threading
import time
from utils.patterns import *
from termcolor import colored

def digestion(func):
	def inner(*args, **kwargs):
		result = func(*args, **kwargs)
		electronics = Electronics.instance()
		electronics.digest()
		return result

	return inner

def monitor(electronics, control):
	while(True)
		electronics.ser.write('t') # temperature
		control.sensors.temperature = electronics.ser.readline()
		
		time.sleep(2)

def watch_once(owner, expr, action):
	electronics = Electronics.instance()
	electronics.watch_once(*args, **kwargs)

class Watch(object):
	def __init__(self, expr, action, initial_value=None, limit=None, owner=None):
		if not isinstance(expr, str): raise Exception("expr must be string")
		if not isinstance(action, types.FunctionType): raise Exception("action must be function")

		self.expr = expr
		self.action = action
		self.prev_value = initial_value
		self.limit = limit
		self.owner = None

@Singleton
class Electronics(object):
	def __init__(self):
		import controller
		import serial
		self.ser = serial.Serial('/dev/ttyACM0', 9600)
		self.watches = []
		self.control = controller.Controller.instance()
		self.hook()

	def hook(self):
		self.watch("self.control.ui.buzzer", lambda old, new: self.ser.write('a' if new else 'r'))

		self.task = threading.Thread(target=monitor, args=(self, self.control))
		self.task.daemon = True
		self.task.start()
		time.sleep(1)

	def watch(self, expr, action):
		initial_value = eval(expr)
		self.watches.append(Watch(expr, action, initial_value))

	def watch_once(self, owner, expr, action):
		initial_value = eval(expr)
		self.watches.append(Watch(expr, action, initial_value, 1, owner))

	def digest(self):
		for i in xrange(len(self.watches) - 1, -1, -1):
			watch = self.watches[i]
			owner = self if watch.owner is None else watch.owner
			value = eval(watch.expr)
			if (value == watch.prev_value): continue
			watch.action(watch.prev_value, value)
			watch.prev_value = value
			
			if watch.limit is not None:
				if watch.limit == 0:
					del self.watches[i]
				elif watch.limit > 0: 
					watch.limit -= 1
