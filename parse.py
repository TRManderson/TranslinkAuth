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

def parseCourseList(page):
	soup=BeautifulSoup(page.replace(")\"\"", ")\""))
	rows=soup.find_all('div')
	semesters=[x for x in rows if _rightID(x,"win4divACTION_NBRGP")]
	index=[_withinDate(_pullDates(x.contents[0])[0],_pullDates(x.contents[0])[1]) for x in semesters].index(True)
	rows=soup.find_all('tr')
	courses=[x for x in rows if _rightID(x, "trACTION_NBR$"+str(index))]
	return [_detailify(x) for x in courses]


def _strTimeDiff(start,end):
	startTime=datetime.strptime(start,"%I:%M %p")
	endTime=datetime.strptime(end,"%I:%M %p")
	return int(round((endTime-startTime).seconds/60 /60.0))

def parseTimetable(page):
	soup=BeautifulSoup(page)
	rows=soup.find_all('span')
	courseTitles=[x.contents[0] for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_DESCR$") and x.contents[0].strip()]
	startTimes=[x.contents[0] for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_UQ_START_TM$") and x.contents[0].strip() != ""]
	endTimes=[x.contents[0].strip() for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_UQ_END_TM$") and x.contents[0].strip() != ""]
	timeDiffs=map(_strTimeDiff,startTimes,endTimes)
	tuples=map(lambda x,y: (x,y),courseTitles,timeDiffs)
	return tuples

def _suitableRow(content):
	if content.startswith("<td width=\"40%\"><b>Student Number:</b></td>"):
		return True
	if content.startswith("<td width=\"40%\"><b>Program:</b></td>"):
		return True
	if content.startswith("<td width=\"40%\"><b>Program:</b></td>"):
		return True
	return False

def parseStudyLoad(page):
	soup=BeautifulSoup(page)
	inputs=[x for x in soup.find_all("input") if x["type"]=="radio"]
	try:
		if inputs[0]["checked"] =="checked":
			return inputs[0]["value"]
	except KeyError as e:
		return inputs[1]["value"]