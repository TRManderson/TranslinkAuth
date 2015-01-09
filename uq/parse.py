from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import namedtuple

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
	title=0
	units=0
	for x in spans:
		if _rightID(x,"DESCR$"):
			title=x.contents[0]
			if units!=0:
				break
		if _rightID(x,"RESULTS$"):
			units=x.contents[0]
			if title!=0:
				break
	for x in courseElement.find_all('div'):
		if _rightID(x, "win4divUQ_DRV_TERM_HTMLAREA5"):
			codeDiv=x
			break
	f=open("temp.out","a+")
	f.write(str(codeDiv)+"\n\n\n")
	f.close()
	try:
		code=re.findall("[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]",str(codeDiv))[0]
	except IndexError as e:
		if "No Enrolments Exist" in str(codeDiv):
			return None
		else:
			raise
	return (code, title, units)

def parseCourseList(page):
	soup=BeautifulSoup(page.replace(")\"\"", ")\""))
	rows=soup.find_all('div')
	semesters=[x for x in rows if _rightID(x,"win4divACTION_NBRGP")]
	index=[_withinDate(_pullDates(x.contents[0])[0],_pullDates(x.contents[0])[1]) for x in semesters].index(True)
	rows=soup.find_all('tr')
	courses=[x for x in rows if _rightID(x,"trACTION_NBR$"+str(index))]
	return filter(lambda x:x!=None, [_detailify(x) for x in courses])


def _strTimeDiff(start,end):
	startTime=datetime.strptime(start,"%I:%M %p")
	endTime=datetime.strptime(end,"%I:%M %p")
	return int(round((endTime-startTime).seconds/60 /60.0))

def parseTimetable(page):
	soup=BeautifulSoup(page)
	rows=soup.find_all('span')
	courseTitles=[x.contents[0] for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_DESCR$") and x.contents[0].strip() and x.contents[0].strip() != ""]
	startTimes=[x.contents[0] for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_UQ_START_TM$") and x.contents[0].strip() != ""]
	endTimes=[x.contents[0].strip() for x in rows if _rightID(x,"UQ_DRV_TTBLE_HP_UQ_END_TM$") and x.contents[0].strip() != ""]
	timeDiffs=map(_strTimeDiff,startTimes,endTimes)
	tuples=map(lambda x,y: (x,y),courseTitles,timeDiffs)
	courseDict={}
	setls=set(map(lambda x: x[0],tuples))
	for i in setls:
		courseDict[i]=0
	for title,val in tuples:
		courseDict[title]+=val
	return courseDict

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

def parseMyPage(page):
	soup=BeautifulSoup(page)
	details=[x for x in soup.find_all('div') if _rightID(x,"uq_tpl_bar")]
	detailsv2=[x for x in soup.find_all('div') if _rightID(x,"uqfooter-content")]
	studentNoRegex="[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
	studentno=re.findall(studentNoRegex,details[0].descendants.next().find_next("p").contents[0])[0]
	title=details[0].descendants.next().find_next("p").contents[0].split(" ")[1]
	studentname=str(detailsv2[0].find_all('p')[0]).split("-")[1].split("(")[0].strip()
	return (studentname,studentno,title)

def _addrBlockToTuple(content):
	content=content.find_all('td')
	streetAddr=content[1].contents[0]
	num=streetAddr.split(" ")[0]
	street=" ".join(streetAddr.split(" ")[1:])
	suburb=content[3].contents[0]
	state=content[5].contents[0]
	postcode=str(content[7])[-9:-5]
	return (num, street, suburb, state, postcode)

def parseAddress(page):
	soup=BeautifulSoup(page)
	for x in soup.find_all('div'):
		if _rightID(x,"win0divUQ_DRV_ADDR_UQ_ADDR_SUMM_SEM"):
			semBlock=x
		if _rightID(x,"win0divUQ_DRV_ADDR_UQ_ADDR_SUMM_MAIL"):
			posBlock=x
	sem=_addrBlockToTuple(semBlock)
	pos=_addrBlockToTuple(posBlock)
	if sem==pos:
		return [sem]
	return [sem,pos]

def parsePhone(page):
	soup=BeautifulSoup(page)
	inputLs=[x for x in soup.find_all("input") if _rightID(x,"UQ_DRV_PERSPHON_")]
	return inputLs[0]["value"]

def validateUser(username,password):
	if len(username) !=8:
		raise ValueError("Username is incorrect length")
	if username[0] !="s" and username[0] !="S":
		raise ValueError("Username is in incorrect format")
	else:
		for i in username[1:]:
			if not i.isdigit():
				raise ValueError("Username is in incorrect format")
	if len(password) < 6:
		raise ValueError("Password too short")
