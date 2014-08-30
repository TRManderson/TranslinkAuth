import parse
import pull
from common import *

suburl="/acu"
background="#193869"

class RequestHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="ACU | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=suburl
		data["incorrect"]=False
		data["bgcolor"]=background
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		postVars=self.request.POST
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			data=parse.parseMainPage(browser.response().read())
		except (Exception,ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			print "Error "+str(e)
		return None
		
class Pdf(webapp2.RequestHandler):
	def get(self): 
		return self.redirect(suburl)

	def post(self):
		postVars=self.request.POST
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			data=parse.parseMainPage(browser.response().read())
		except (Exception,ValueError) as e:
			data={}
			data["title"]="ACU | No TTCC?"
			data["extra"]=""
			data["usr"]=""
			data["suburl"]=suburl
			data["incorrect"]=False
			data["bgcolor"]=background
			data["extradetails"]=""
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			print "Error "+str(e)
		for k,v in parse.parseInformation(pull.pullInformation(browser)).iteritems():
			data[k]=v
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())
