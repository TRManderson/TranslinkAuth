import webapp2
from parse import *
from pull import *
from collections import namedtuple
from put import landing,proof
from paste import httpserver


class index(webapp2.RequestHandler):
	def get(self):
		self.response.write(landing(title="TransAuth"))
	def post(self):
		postVars=self.request.POST
		browser=auth(postVars["username"],postVars["password"])
		studentname,studentno=parseMyPage(pullMyPage(browser))
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

urls = [
	('/', index)
	]

if __name__ == "__main__":
	app=webapp2.WSGIApplication(urls,debug=True)
	httpserver.serve(app, host='127.0.0.1', port='8080')