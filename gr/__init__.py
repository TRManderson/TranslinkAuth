import parse
import pull
from common import *

class ReqHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="Griffith | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]="/gr"
		data["incorrect"]=False
		data["bgcolor"]="#D00"
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		data={}
		data["title"]="Griffith | No TTCC?"
		data["suburl"]="/gr"
		data["extradetails"]=""
		data["bgcolor"]="#D00"
		postVars=self.request.POST
		try:
			parse.validateUser(username,password)
			browser=pull.auth(postVars["username"],postVars["password"])
			name=gr.parseMainPage(browser.response().read())
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		data["studentname"]=name
		data["studentno"]=postVars["username"][1:]
		ttData=parse.parseTimetable(pull.pullTimetable(browser))
		if ttData[1]:
			data["enrollment"]="Full Time"
		else:
			data["enrollment"]="Part Time"
		data["courselist"]=[Course(code=i[0],title=i[1],hours=i[2]) for i in ttData[0]]
		if data["enrollment"]=="Full Time" or sum(map(lambda x: x.hours,data["courselist"])) >=12:
			data["eligible"]=True
		else:
			data["eligible"]=False
		self.response.write(proof.render(**data))


class Pdf(webapp2.RequestHandler):
	def post(self):
		postVars=self.request.POST
		data={}
		try:
			parse.validateUser(username,password)
			name=gr.parseMainPage(browser.response().read())
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		browser=pull.auth(postVars["username"],postVars["password"])
		data=parse.parseInfo(pull.pullInformation(browser))
		data["university"]="Griffith University"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())