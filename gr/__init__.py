import parse
import pull
from common import *

background="#D00"
suburl="/gr"

class ReqHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="Griffith | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=suburl
		data["incorrect"]=False
		data["bgcolor"]=background
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		data={}
		data["title"]="Griffith | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=suburl
		data["incorrect"]=False
		data["bgcolor"]=background
		data["extradetails"]=""
		postVars=self.request.POST
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			name=parse.parseMainPage(browser.response().read())
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			print "Error "+str(e)
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
		data["title"]="Griffith | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=suburl
		data["incorrect"]=False
		data["bgcolor"]=background
		data["extradetails"]=""
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			name=parse.parseMainPage(browser.response().read())
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			print "Error "+str(e)
			self.response.write(signin.render(**data))
			return
		data=parse.parseInfo(pull.pullInformation(browser))
		data["university"]="Griffith University"
		data["surname"]=name.split()[-1]
		data["givennames"]=" ".join(name.split()[:-1])
		data["studentno"]=postVars["username"][1:]
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())