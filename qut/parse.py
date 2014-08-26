from bs4 import BeautifulSoup,Tag
from datetime import datetime

def _rightProp(x,match, prop):
	try:
		xID=x[prop]
	except:
		return False
	if type(xID) == list:
		return [x.startswith(match) for x in xID][0]
	else:
		return xID.startswith(match)

def parseMainPage(page):
	soup=BeautifulSoup(page)
	for x in soup.find_all('h2'):
		if _rightProp(x,"user-greeting","class"):
			return x.contents[1].contents[0]

def _parseTimeDiff(diffstr):
	split = diffstr.split("-")
	start=datetime.strptime(split[0],"%I:%M%p")
	end=datetime.strptime(split[1],"%I:%M%p")
	return int(round((end-start).seconds/60 /60.0))

def parseTimetable(page):
	soup=BeautifulSoup(page)
	unitsElems=[x for x in soup.find_all('tr') if _rightProp(x,"unit-detail","class")]
	units = [(y[0].contents[0],y[1].contents[0].contents[0]) for y in [x.find_all('td')[0:2] for x in unitsElems]]
	courses=[]
	for i in range(len(units)):
		courses+=[0]
	for i,e in enumerate(unitsElems):
		for j in e.nextSiblingGenerator():
			try:
				if "unit-detail" in j["class"]:
					break
				if "class-detail" in j["class"]:
					courses[i]+=sum([_parseTimeDiff(x.contents[0]) for x in j.find_all('td') if _rightProp(x,"class-time","class")])
			except KeyError:
				pass
	return map(lambda x,y:(x[0],x[1],y),units,courses)

def _addrStrToParts(addrStr):
	data={}
	split=addrStr.split(" ")[:-1]
	data["unit/num"]=split[0]
	data["postcode"]=split[-1]
	data["state"]=split[-2]
	split=split[1:-2]
	data["suburb"]=" ".join([x for x in split if x.isupper()])
	data["street"]=" ".join([x for x in split if not x.isupper()])
	return data

def _nthGenElem(generator,n):
	for i in range(n+1):
		x=generator.next()
	return x

def parseInfo(page):
	soup=BeautifulSoup(page)
	tables=soup.find_all('table')
	data={}
	for x in tables:
		if _rightProp(x,"ctl00_Content_grdAddresses","id"):
			addrTable=x
		elif _rightProp(x,"ctl00_Content_grdPhones","id"):
			phoneTable=x
		elif _rightProp(x,"ctl00_Content_grdEmails","id"):
			emailTable=x
		else:
			continue
	addrStrs=[_nthGenElem(x.children,3).contents[0] for x in list(_nthGenElem(addrTable.children,2).children)[1:-1]]
	for k,v in _addrStrToParts(addrStrs[1]).iteritems():
		data["res"+k]=v
	if addrStrs[0] == addrStrs[1]:
		data["as_above"]=True
	else:
		for k,v in _addrStrToParts(addrStrs[0]).iteritems():
			data["post"+k]=v
		data["postaddress"]=data["postunit/num"]+" "+data["poststreet"]
	data["phone"]=_nthGenElem(_nthGenElem(_nthGenElem(phoneTable.children,2).children,1).children,3).contents[0]
	data["email"]=_nthGenElem(_nthGenElem(_nthGenElem(emailTable.children,2).children,1).children,3).contents[1].contents[0]
	return data


def parseEnrollment(page):
	soup=BeautifulSoup(page)
	for x in soup.find_all('table'):
		if _rightProp(x,"ctl00_Content_grdCurrEnrol",'id'):
			table=x.find('tbody')
	units=0
	for i in table.contents[1:-1]:
		units+=int(_nthGenElem(i.children,6).contents[0])
	if units>=36:
		return True
	return False

def validateUser(username,password):
	if len(username) < 8:
		raise ValueError("Username too short")
	if len(username) > 9:
		raise ValueError("Username too long")
	if username[0] != "n" and username[0] != "N":
		raise ValueError("Username in incorrect format")
	else:
		for digit in username[1:]:
			if not (digit.isdigit()):
				raise ValueError("Username in incorrect format")
	if len(password) <6:
		raise ValueError("Password too short")
	return
