import webapp2
import uq
import gr
import qut
from mako.template import Template
from mako.lookup import TemplateLookup

lookup=TemplateLookup(directories=[".","./templates/"])
landing=Template(filename="templates/landing.mako",lookup=lookup)
aboutpage=Template(filename="templates/about.mako",lookup=lookup)

class index(webapp2.RequestHandler):
	def get(self):
		self.response.write(landing.render(title="No TTCC?",bgcolor="#68a427"))

class about(webapp2.RequestHandler):
	def get(self):
		self.response.write(aboutpage.render(title="About No TTCC?",bgcolor="#68a427"))

class favicon(webapp2.RequestHandler):
	def get(self):
		f=open('favicon.ico','rb')
		self.response.headers['Content-Type'] ="image/x-icon"
		self.response.write(f.read())
		f.close()

urls = [
	('/', index),
	('/about', about),
	('/uq',uq.ReqHandler),
	('/gr',gr.ReqHandler),
	('/qut',qut.ReqHandler),
	('/qut/ttcc.pdf',qut.Pdf),
	('/uq/ttcc.pdf',uq.Pdf),
	('/gr/ttcc.pdf',gr.Pdf),
	('/favicon.ico',favicon)
	]

app=webapp2.WSGIApplication(urls,debug=True)
