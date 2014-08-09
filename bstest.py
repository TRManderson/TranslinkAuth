from bs4 import BeautifulSoup
from datetime import datetime
url="https://www.sinet.uq.edu.au/psc/ps_4/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_CRSE_HOME.GBL"
f=open("test.html")
page=f.read()
f.close()


def rightRow(x,id):
	try:
		xID=x["id"]
	except:
		return False
	return xID.startswith(id)

def pulldates(semstring):
	return semstring.split("(")[1].split(";")[0].split("-")

def withinDate(startdatestr,enddatestr):
	startdate=[int(x) for x in startdatestr.split("/")]
	startdate=datetime(startdate[2],startdate[1],startdate[0])
	enddate=[int(x) for x in enddatestr.split("/")]
	enddate=datetime(enddate[2], enddate[1], enddate[0])
	now = datetime.now()
	if startdate < now and now < enddate:
		return True
	return False




def parsePage(page):
	soup=BeautifulSoup(page)
	rows=soup.find_all('div')
	semesters=[x.contents[0] for x in rows if rightRow(x,"win4divACTION_NBRGP")]
	index=[withinDate(pulldates(x)[0],pulldates(x)[1]) for x in semesters].index(True)