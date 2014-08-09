from bs4 import BeautifulSoup
from datetime import datetime
import re

def _rightID(x,id):
	try:
		xID=x["id"]
	except:
		return False
	return xID.startswith(id)

def _pullDates(semstring):
	return semstring.split("(")[1].split(";")[0].split("-")

def _withinDate(startdatestr,enddatestr):
	startdate=[int(x) for x in startdatestr.split("/")]
	startdate=datetime(startdate[2],startdate[1],startdate[0])
	enddate=[int(x) for x in enddatestr.split("/")]
	enddate=datetime(enddate[2], enddate[1], enddate[0])
	now = datetime.now()
	if startdate < now and now < enddate:
		return True
	return False

def _detailify(courseElement):
	spans = courseElement.find_all('span')
	title=[x for x in spans if _rightID(x,"DESCR$")][0].contents[0]
	units=[x for x in spans if _rightID(x,"RESULTS$")][0].contents[0]
	codeDiv=[x for x in courseElement.find_all('div') if _rightID(x, "win4divUQ_DRV_TERM_HTMLAREA5")][0]
	code=re.findall("[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]",str(codeDiv))[0]
	return (code, title, units)

def parsePage(page, returnType="courses"):
	soup=BeautifulSoup(page.replace(")\"\"", ")\""))
	rows=soup.find_all('div')
	semesters=[x for x in rows if _rightID(x,"win4divACTION_NBRGP")]
	index=[_withinDate(_pullDates(x.contents[0])[0],_pullDates(x.contents[0])[1]) for x in semesters].index(True)
	rows=soup.find_all('tr')
	courses=[x for x in rows if _rightID(x, "trACTION_NBR$"+str(index))]
	if returnType == "courses":
		return [_detailify(x) for x in courses]
	elif returnType == "timetableHours":
		return None

