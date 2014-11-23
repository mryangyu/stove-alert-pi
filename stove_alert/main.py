from datetime import datetime
import cherrypy

from controls.electronics import Electronics
from controls.controller import Controller

electronics = Electronics.instance()
control = Controller.instance()

class WebService(object):
	exposed = True

class ControllerService(WebService):
	def GET(self):
		return control.to_JSON()

class RootService(WebService):
	control = ControllerService()

	def GET(self):
		return "Hello!"

	def PUT(self, **kw):
		electronics.commands(kw)
		return control.to_JSON()

if __name__ == "__main__":
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': False,
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		}
	}
	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 8090}
		)
	cherrypy.quickstart(RootService(), '/', conf)