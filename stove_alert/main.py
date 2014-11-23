from datetime import datetime
import cherrypy

from controls.electronics import Electronics
from controls.controller import Controller

electronics = Electronics.instance()
control = Controller.instance()
control.initialize_components()

class WebService(object):
	exposed = True

class ControllerService(WebService):
	def GET(self):
		return control.to_JSON()

class RootService(WebService):
	control = ControllerService()

	def GET(self):
		return "Hello!"

if __name__ == "__main__":
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': False,
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		}
	}

	cherrypy.quickstart(RootService(), '/', conf)