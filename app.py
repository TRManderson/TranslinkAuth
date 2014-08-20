import webapp2
import uq
import gr
import qut
import pypdftk
from collections import namedtuple
from paste import httpserver
from mako.template import Template
from mako.lookup import TemplateLookup

lookup=TemplateLookup(directories=[".","./templates/"])
signin=Template(filename="templates/signin.mako",lookup=lookup)
proof=Template(filename="templates/proof.mako",lookup=lookup)
landing=Template(filename="templates/landing.mako",lookup=lookup)
aboutpage=Template(filename="templates/about.mako",lookup=lookup)

Course = namedtuple("Course",["code","title","hours"])

def fillPdf(kwargs):
	try:
		pdfData={}
		try:
			if kwargs["title"]=="Mr":
				pdfData["RB2"]=1
			elif kwargs["title"]=="Mrs":
				pdfData["RB2"]=2
			elif kwargs["title"]=="Miss":
				pdfData["RB2"]=3
			elif kwargs["title"]=="Ms":
				pdfData["RB2"]=4
			else:
				pdfData["Text2"]=kwargs["title"]
				pdfData["RB2"]=5
		except KeyError:
			pass
		pdfData["Text3"]=kwargs["surname"]
		pdfData["Text4"]=kwargs["givennames"]
		pdfData["Text5"]=kwargs["university"]
		pdfData["SN1"]=kwargs["studentno"]
		pdfData["Text6"]=kwargs["resunit/num"]
		pdfData["Text7"]=kwargs["resstreet"]
		pdfData["Text8"]=kwargs["ressuburb"]
		pdfData["Text9"]=kwargs["resstate"]
		pdfData["Text10"]=kwargs["respostcode"]
		if kwargs["as_above"]==True:
			pdfData["Text11"]="As above"
		else:
			pdfData["Text11"]=kwargs["postaddress"]
			pdfData["Text12"]=kwargs["postsuburb"]
			pdfData["Text13"]=kwargs["poststate"]
			pdfData["Text14"]=kwargs["postpostcode"]
		pdfData["Text15"]=kwargs["phone"]
		pdfData["Text16"]=kwargs["email"]
		now=datetime.now()
		pdfData["Text17"]=now.day
		pdfData["Text18"]=now.month
		pdfData["Text19"]=now.year
	except Exception:
		pass
	newfile=pypdftk.fill_form("./new.pdf",pdfData)
	f=open(newfile,"rb")
	return f


class uqReqHandler(webapp2.RequestHandler):
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
			uq.parse.validateUser(postVars["username"],postVars["password"])
			browser=uq.pull.auth(postVars["username"],postVars["password"])
			data["studentname"],data["studentno"],useless=uq.parse.parseMyPage(uq.pull.pullMyPage(browser))
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		ttlist=uq.parse.parseTimetable(uq.pull.pullTimetable(browser))
		cl=uq.parse.parseCourseList(uq.pull.pullCourses(browser))
		data["courselist"]=[]
		for i in cl:
			try:
				hours=ttlist[i[1]]
			except KeyError:
				hours=0
			data["courselist"]+=[Course(code=i[0],title=i[1],hours=hours)]
		if uq.parse.parseStudyLoad(uq.pull.pullStudyLoad(browser)) =="F":
			data["enrollment"]="Full Time"
		else:
			data["enrollment"]="Part Time"
		if data["enrollment"]=="Full Time" or sum(map(lambda x: x.hours,courseList)) >=12:
			data["eligible"]=True
		else:
			data["eligible"]=False
		
		self.response.write(proof.render(**data))

class uqPdf(webapp2.RequestHandler):
	def post(self):
		data={}
		postVars=self.request.POST
		browser=uq.pull.auth(postVars["username"],postVars["password"])
		data["university"]="University of Queensland"
		try:
			x=uq.parse.parseMyPage(uq.pull.pullMyPage(browser))
			fullname=x[0]
			data["surname"]=fullname.split(" ")[-1]
			data["givennames"]=" ".join(fullname.split(" ")[:-1])
			data["studentno"]=x[1]
			data["title"]=x[2]
		except Exception as e:
			errorMessage="<p class=\"text-danger\">Invalid username or password</p>"
			self.response.write(landing(title="TransAuth",extra=errorMessage,usr=postVars["username"],incorrect=True))
			return
		addresses=uq.parse.parseAddress(uq.pull.pullAddress(browser))
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
		data["phone"]=uq.parse.parsePhone(uq.pull.pullPhone(browser))
		data["email"]=postVars["username"]+"@student.uq.edu.au"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())


class grReqHandler(webapp2.RequestHandler):
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
		browser=gr.pull.auth(postVars["username"],postVars["password"])
		try:
			name=gr.parseMainPage(browser.response().read())
			gr.parse.validateUser(username,password)
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
		ttData=gr.parse.parseTimetable(gr.pull.pullTimetable(browser))
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


class grPdf(webapp2.RequestHandler):
	def post(self):
		postVars=self.request.POST
		data={}
		try:
			name=gr.parseMainPage(browser.response().read())
			gr.parse.validateUser(username,password)
		except (Exception, ValueError) as e:
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		browser=gr.pull.auth(postVars["username"],postVars["password"])
		data=gr.parse.parseInfo(gr.pull.pullInformation(browser))
		data["university"]="Griffith University"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())


class qutReqHandler(webapp2.RequestHandler):
	background="#00467f"
	suburl="/qut"
	def get(self):
		data={}
		data["title"]="QUT | No TTCC?"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]=self.suburl
		data["incorrect"]=False
		data["bgcolor"]=self.background
		data["extradetails"]=""
		self.response.write(signin.render(**data))

	def post(self):
		data={}
		data["title"]="QUT | No TTCC?"
		data["suburl"]=self.suburl
		data["extradetails"]=""
		data["bgcolor"]=self.background
		postVars=self.request.POST
		try:
			qut.parse.validateUser(postVars["username"],postVars["password"])
			browser=qut.pull.auth(postVars["username"],postVars["password"])
			name=qut.parse.parseMainPage(qut.pull.pullMainPage(browser))
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
		ttData=qut.parse.parseTimetable(qut.pull.pullTimetable(browser))
		if qut.parse.parseEnrollment(qut.pull.pullEnrollment(browser)):
			data["enrollment"]="Full Time"
		else:
			data["enrollment"]="Part Time"
		data["courselist"]=[Course(code=i[0],title=i[1],hours=i[2]) for i in ttData]
		if data["enrollment"]=="Full Time" or sum(map(lambda x: x.hours,data["courselist"])) >=12:
			data["eligible"]=True
		else:
			data["eligible"]=False
		self.response.write(proof.render(**data))

class qutPdf(webapp2.RequestHandler):
	suburl="/qut"
	background="#00467f"
	def get(self):
		return self.redirect(self.suburl)

	def post(self):
		postVars=self.request.POST
		try:
			qut.parse.validateUser(postVars["username"],postVars["password"])
			browser=qut.pull.auth(postVars["username"],postVars["password"])
			name=qut.parse.parseMainPage(qut.pull.pullMainPage(browser))
		except (Exception, ValueError) as e:
			data={}
			data["title"]="QUT | No TTCC?"
			data["suburl"]=self.suburl
			data["extradetails"]=""
			data["bgcolor"]=self.background
			data["usr"]=postVars["username"]
			if type(e)==ValueError:
				data["extra"]="<p class=\"text-danger\">"+str(e)+"</p>"
			else:
				data["extra"]="<p class=\"text-danger\">Invalid username or password</p>"
				
			data["incorrect"]=True
			self.response.write(signin.render(**data))
			return
		name=name.replace(" - ","-")
		data=qut.parse.parseInfo(qut.pull.pullInformation(browser))
		data["surname"]=name.split()[-1]
		data["studentno"]=postVars["username"][1:]
		data["givennames"]=" ".join(name.split()[:-1])
		data["university"]="Queensland University of Technology"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())


class index(webapp2.RequestHandler):
	def get(self):
		self.response.write(landing.render(title="No TTCC?",bgcolor="#68a427"))

class about(webapp2.RequestHandler):
	def get(self):
		self.response.write(aboutpage.render(title="About No TTCC?",bgcolor="#68a427"))


urls = [
	('/', index),
	('/about', about),
	('/uq',uqReqHandler),
	('/gr',grReqHandler),
	('/qut',qutReqHandler),
	('/qut/ttcc.pdf',qutPdf),
	('/uq/ttcc.pdf',uqPdf),
	('/gr/ttcc.pdf',grPdf),
	]

if __name__ == "__main__":
	app=webapp2.WSGIApplication(urls,debug=True)
	httpserver.serve(app, host='0.0.0.0', port='8080')
