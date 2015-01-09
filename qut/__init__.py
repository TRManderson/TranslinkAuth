import pull
import parse
from common import *

background="#00467f"
suburl="/qut"

class ReqHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="QUT | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=suburl
		data["incorrect"]=False
		data["bgcolor"]=background
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		data={}
		data["title"]="QUT | No TTCC?"
		data["suburl"]=suburl
		data["extradetails"]=""
		data["bgcolor"]=background
		postVars=self.request.POST
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			print "Error "+str(e)
			return
		for k,v in parse.parseEnrollment(pull.pullEnrollment(browser)).iteritems():
			data[k]=v
		data["studentno"]=postVars["username"][1:]
		ttData=parse.parseTimetable(pull.pullTimetable(browser))
		data["courselist"]=[Course(code=i[0],title=i[1],hours=i[2]) for i in ttData]
		if data["enrollment"]=="Full Time" or sum(map(lambda x: x.hours,data["courselist"])) >=12:
			data["eligible"]=True
		else:
			data["eligible"]=False
		self.response.write(proof.render(**data))

class Pdf(webapp2.RequestHandler):
	def get(self):
		return self.redirect(suburl)

	def post(self):
		postVars=self.request.POST
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			data=parse.parseInfo(pull.pullInformation(browser))
		except (Exception, ValueError) as e:
			data={}
			data["title"]="QUT | No TTCC?"
			data["suburl"]=suburl
			data["extradetails"]=""
			data["bgcolor"]=background
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			print "Error "+str(e)
			return
		data["university"]="Queensland University of Technology"
		data["studentno"]=postVars["username"][1:]
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())
