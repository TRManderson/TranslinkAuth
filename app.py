import webapp2
from parse import *
from pull import *
from collections import namedtuple
from put import landing,proof
from paste import httpserver


class index(webapp2.RequestHandler):
	def get(self):
		self.response.write(landing(title="TransAuth",extra="",usr="",incorrect=False))


	def post(self):
		postVars=self.request.POST
		browser=auth(postVars["username"],postVars["password"])
		try:
			studentname,studentno,useless=parseMyPage(pullMyPage(browser))
		except Exception as e:
			errorMessage="<p class=\"text-danger\">Invalid username or password</p>"
			self.response.write(landing(title="TransAuth",extra=errorMessage,usr=postVars["username"],incorrect=True))
			return
		ttlist=parseTimetable(pullTimetable(browser))
		cl=parseCourseList(pullCourses(browser))
		Course = namedtuple("Course",["code","title","hours"])
		f=open("debug.log","a+")
		f.write(str(ttlist)+"\n")
		courseList=[]
		for i in cl:
			try:
				hours=ttlist[i[1]]
			except KeyError:
				hours=0
			courseList+=[Course(code=i[0],title=i[1],hours=hours)]
		if parseStudyLoad(pullStudyLoad(browser)) =="F":
			enrollment="Full Time"
		else:
			enrollment="Part Time"
		if enrollment=="Full Time" or sum(map(lambda x: x.hours,courseList)) >=12:
			eligible=True
		else:
			eligible=False
		self.response.write(proof(title="TransAuth",courselist=courseList,enrollment=enrollment, studentname=studentname,studentno=studentno,eligible=eligible))

class pdf(webapp2.RequestHandler):
	def post(self):
		data={}
		browser=auth(postVars["username"],postVars["password"])
		try:
			x=parseMyPage(pullMyPage(browser))
			fullname=x[0]
			data["surname"]=fullname.split(" ")[-1]
			data["givennames"]=" ".join(fullname.split(" ")[:-1])
			data["studentno"]=x[1]
			data["title"]=x[2]
		except Exception as e:
			errorMessage="<p class=\"text-danger\">Invalid username or password</p>"
			self.response.write(landing(title="TransAuth",extra=errorMessage,usr=postVars["username"],incorrect=True))
			return
		addresses=parseAddress(pullAddress(browser))
		if len(addresses)!=1:
			data["as_above"]="F"
			pos=addresses[1]
			data["postaddress"] =pos[0]+" "+pos[1]
			data["postsuburb"]=pos[2]
			data["poststate"]=pos[3]
			data["postpostcode"]=pos[4]
		else:
			data["as_above"]="T"
		addr=addresses[0]
		data["resunit/num"]=pos[0]
		data["resstreet"]=pos[1]
		data["ressuburb"]=pos[2]
		data["resstate"]=pos[3]
		data["respostcode"]=pos[4]


urls = [
	('/', index)
	('/ttcc.pdf',pdf)
	]

if __name__ == "__main__":
	app=webapp2.WSGIApplication(urls)
	httpserver.serve(app, host='0.0.0.0', port='8080')