import pull
import parse
from common import *

class ReqHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="UQ | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["incorrect"]=False
		data["suburl"]="/uq"
		data["bgcolor"]="#240330"
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		postVars=self.request.POST
		data={"title":"UQ | No TTCC?"}
		data["bgcolor"]="#240330"
		data["suburl"]="/uq"
		data["extradetails"]=""
		try:
			parse.validateUser(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])
			data["studentname"],data["studentno"],useless=parse.parseMyPage(pull.pullMyPage(browser))
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		ttlist=parse.parseTimetable(pull.pullTimetable(browser))
		cl=parse.parseCourseList(pull.pullCourses(browser))
		data["courselist"]=[]
		for i in cl:
			try:
				hours=ttlist[i[1]]
			except KeyError:
				hours=0
			data["courselist"]+=[Course(code=i[0],title=i[1],hours=hours)]
		if parse.parseStudyLoad(pull.pullStudyLoad(browser)) =="F":
			data["enrollment"]="Full Time"
		else:
			data["enrollment"]="Part Time"
		if data["enrollment"]=="Full Time" or sum(map(lambda x: x.hours,courseList)) >=12:
			data["eligible"]=True
		else:
			data["eligible"]=False
		
		self.response.write(proof.render(**data))

class Pdf(webapp2.RequestHandler):
	def post(self):
		data={}
		postVars=self.request.POST
		data["university"]="University of Queensland"
		try:
			parse.validate(postVars["username"],postVars["password"])
			browser=pull.auth(postVars["username"],postVars["password"])

			x=parse.parseMyPage(pull.pullMyPage(browser))
			fullname=x[0]
			data["surname"]=fullname.split(" ")[-1]
			data["givennames"]=" ".join(fullname.split(" ")[:-1])
			data["studentno"]=x[1]
			data["title"]=x[2]
		except Exception as e:
			errorMessage="<p class=\"text-danger\">Invalid username or password</p>"
			self.response.write(landing.render(title="TransAuth",extra=errorMessage,usr=postVars["username"],incorrect=True))
			return
		addresses=parse.parseAddress(pull.pullAddress(browser))
		if len(addresses)!=1:
			data["as_above"]="F"
			pos=addresses[1]
			data["postaddress"] =pos[0]+" "+pos[1]
			data["postsuburb"]=pos[2]
			data["poststate"]=pos[3]
			data["postpostcode"]=pos[4]
		else:
			data["as_above"]=True
		pos=addresses[0]
		data["resunit/num"]=pos[0]
		data["resstreet"]=pos[1]
		data["ressuburb"]=pos[2]
		data["resstate"]=pos[3]
		data["respostcode"]=pos[4]
		data["phone"]=parse.parsePhone(pull.pullPhone(browser))
		data["email"]=postVars["username"]+"@student.uq.edu.au"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())