import webapp2
import uq
import gr
from collections import namedtuple
from paste import httpserver
from mako.template import Template
from mako.lookup import TemplateLookup

lookup=TemplateLookup(directories=[".","./templates/"])
signin=Template(filename="templates/signin.mako",lookup=lookup)
proof=Template(filename="templates/proof.mako",lookup=lookup)

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
		pdfData["Text17"]=now.strftime("%d")
		pdfData["Text18"]=now.strftime("%m")
		pdfData["Text19"]=now.strftime("%y")
	except Exception:
		pass
	newfile=pypdftk.fill_form("./new.pdf",pdfData)
	f=open(newfile,"rb")
	return f


class uqReqHandler(webapp2.RequestHandler):
	def get(self):
		data={}
		data["title"]="Translink Auth"
		data["extra"]=""
		data["usr"]=""
		data["incorrect"]=False
		data["suburl"]="/uq"
		data["bgcolor"]="#240330"
		self.response.write(signin.render(**data))

	def post(self):
		postVars=self.request.POST
		browser=uq.pull.auth(postVars["username"],postVars["password"])
		data={"title":"Translink Auth"}
		data["bgcolor"]="#240330"
		data["suburl"]="/uq"
		try:
			data["studentname"],data["studentno"],useless=uq.parse.parseMyPage(uq.pull.pullMyPage(browser))
		except Exception:
			data["usr"]=postVars["username"]
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
		browser=uq.pull.pullauth(postVars["username"],postVars["password"])
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
		data["title"]="Translink Auth"
		data["extra"]=""
		data["usr"]=""
		data["suburl"]="/gr"
		data["incorrect"]=False
		data["bgcolor"]="#24033"
		self.response.write(signin.render(**data))

	def post(self):
		data={}
		postVars=self.request.POST
		browser=gr.pull.auth(postVars["username"],postVars["password"])
		name=gr.parseMainPage(browser.response().read())
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
		browser=gr.pull.auth(postVars["username"],postVars["password"])
		data=gr.parse.parseInfo(gr.pull.pullInformation(browser))
		data["university"]="Griffith University"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = "attachment;filename=ttcc.pdf"
		self.response.write(fillPdf(data).read())

class index(webapp2.RequestHandler):
	def get(self):
		self.response.write("hi")


urls = [
	('/', index),
	('/uq',uqReqHandler),
	('/gr',grReqHandler),
	('/uq/ttcc.pdf',uqPdf),
	('/gr/ttcc.pdf',grPdf),
	]

if __name__ == "__main__":
	app=webapp2.WSGIApplication(urls)
	httpserver.serve(app, host='0.0.0.0', port='8080')
