from bs4 import BeautifulSoup
from datetime import datetime
from re import match

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
	return [x for x in soup.find_all("td") if _rightProp(x,"GU_STYLE_CLASS_9","class")][0].contents[0].contents[0]

def _addrStringToParts(addrStr):
	addrDict={}
	broad=addrStr[1].split(" ")
	addrDict["postcode"]=broad[-2]
	addrDict["state"]=broad[-3]
	addrDict["suburb"]=" ".join(broad[0:-3])
	narrow=addrStr[0].split(" ")
	addrDict["unit/num"]=narrow[0]
	addrDict["street"]=" ".join(narrow[1:])
	return addrDict

def _parsePhone(phoneStr):
	return "".join("".join(phoneStr.split("/")).split("-"))

def parseInfo(page):
	soup=BeautifulSoup(page)
	infoDict={}
	spans=soup.find_all('span')
	infoDict["email"]=[x for x in spans if _rightProp(x,"DERIVED_SSS_SCL_EMAIL_ADDR","id")][0].contents[0]
	infoDict["phone"]=_parsePhone([x for x in spans if _rightProp(x,"DERIVED_SSS_SCL_DESCR50","id")][0].contents[0])
	resAddr=[x.contents for x in spans if _rightProp(x,"DERIVED_SSS_SCL_SSS_LONGCHAR_1","id")][0]
	resAddr=[resAddr[0].strip(),resAddr[2].strip()]
	posAddr=[x.contents for x in spans if _rightProp(x,"DERIVED_SSS_SCL_SSS_LONGCHAR_2","id")][0]
	posAddr=[posAddr[0].strip(),posAddr[2].strip()]
	for k,v in _addrStringToParts(resAddr).iteritems():
		infoDict["res"+k]=v
	if resAddr !=posAddr:
		for k,v in _addrStringToParts(posAddr).iteritems():
			infoDict["post"+k]=v
	else:
		infoDict["as_above"]=True
	return infoDict


def _parseTimeDiff(diffstr):
	split = diffstr.split(" - ")
	start=datetime.strptime(split[0],"%I:%M%p")
	end=datetime.strptime(split[1],"%I:%M%p")
	return int(round((end-start).seconds/60 /60.0))

def _ttDetailsFromDiv(divBlock):
	tcsplit=divBlock.find_all("td")[0].contents[0].split(" - ")
	stuff=set([" ".join(x.contents[0].strip().split(" ")[1:]) for x in divBlock.find_all("span") if _rightProp(x,"MTG_SCHED$","id")])
	hours=sum(map(lambda x:_parseTimeDiff(x),stuff))
	return(tcsplit[0].strip(), " ".join(tcsplit[1:]).strip(), hours)

def parseTimetable(page):
	from pull import writeOut
	soup=BeautifulSoup(page)
	tuples=[_ttDetailsFromDiv(x) for x in soup.find_all("div") if _rightProp(x,"win0divDERIVED_REGFRM1_DESCR20","id")]
	eqLoad=float([x for x in soup.find_all('span') if _rightProp(x,"DERIVED_SR_SSR_TOT_EFTSU_LD","id")][0].contents[0].strip())
	if eqLoad >= 0.5:
		ft=True
	else:
		ft=False
	return (tuples,ft)

def validateUser(username,password):
	if len(username) != 8:
		print username
		raise ValueError("Username incorrect length")
	if len(password) < 6:
		print password
		raise ValueError("Password too short")
	if username[0] !="s" and username[0] !="S":
		print username
		raise ValueError("Username is in incorrect format")
	else:
		for i in username[1:]:
			if not i.isdigit():
				print username
				raise ValueError("Username is in incorrect format")
	return