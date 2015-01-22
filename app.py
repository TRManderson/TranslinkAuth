import webapp2
import uq
import qut
import gr
from mako.template import Template
from mako.lookup import TemplateLookup

lookup=TemplateLookup(directories=[".","./templates/"])
landing=Template(filename="templates/landing.mako",lookup=lookup)
aboutpage=Template(filename="templates/about.mako",lookup=lookup)
grifwarning=Template(filename="templates/grifwarning.mako",lookup=lookup)

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

class loading(webapp2.RequestHandler):
	def get(self):
		f=open('loading.gif','rb')
		self.response.headers['Content-Type'] ="image/gif"
		self.response.headers['Cache-Control']="max-age=31536000;"
		self.response.write(f.read())
		f.close()

class grWarn(webapp2.RequestHandler):
	def get(self):

		self.response.write(grifwarning.render(title="Griffith | No TTCC?",bgcolor="#D00"))

urls = [
	('/', index),
	('/about', about),
	('/uq',uq.ReqHandler),
	('/gr',gr.ReqHandler),
	('/gr/warn',grWarn),
	('/qut',qut.ReqHandler),
	('/qut/ttcc.pdf',qut.Pdf),	
	('/uq/ttcc.pdf',uq.Pdf),
	('/gr/ttcc.pdf',gr.Pdf),
	('/favicon.ico',favicon),
	('/loading.gif',loading),
	]

app=webapp2.WSGIApplication(urls,debug=True)
if __name__=="__main__":
	from paste import httpserver
	httpserver.serve(app)
