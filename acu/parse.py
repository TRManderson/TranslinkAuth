from bs4 import BeautifulSoup
from re import findall

def _rightProp(x,match, prop):
	try:
		xID=x[prop]
	except:
		return False
	if type(xID) == list:
		return [x.startswith(match) for x in xID][0]
	else:
		return xID.startswith(match)

def _nthGenElem(generator,n):
	for i in range(n+1):
		x=generator.next()
	return x

def _addrBlockToDict(addrBlock):
	streetaddr=addrBlock.contents[0].strip().replace("&nbsp"," ").split(" ")
	substatepost=[x.strip() for x in addrBlock.contents[2].strip().replace("&nbsp"," ").split(",")]
	return {"unit/num":streetaddr[0],"street":" ".join(streetaddr[1:]),"suburb":substatepost[0],"state":substatepost[1].split()[0],"postcode":substatepost[1].split()[1]}


def parseInformation(page):
	soup=BeautifulSoup(page)
	x=soup.find('table')
	while not _rightProp(x,"datadisplaytable","class"):
		x=x.find_next('table')
	x=[a for a in x.find_all('tr') if not _rightProp(_nthGenElem(a.children,1),"ddseparator","class")]
	data={}
	for i in range(len(x)/3):
		addrType=_nthGenElem(x[i*3].children,1).contents[0]
		addrBlock=_nthGenElem(x[i*3 +2].children,3)
		_data=_addrBlockToDict(addrBlock)
		if addrType=="Mailing Address":
			for k,v in _data.iteritems():
				data["post"+k]=v
			data["phone"]=findall("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",str(_nthGenElem(x[i*3+2].children,5)))[0]
		elif addrType=="Permanent Residence":
			for k,v in _data.iteritems():
				data["res"+k]=v
	data["as_above"]=True
	for k,v in data.iteritems():
		if k.startswith("post"):
			if not data["res"+k[4:]]==v: 
				data["as_above"]=False
				break
	return data

def parseMainPage(page):
	soup=BeautifulSoup(page)
	for i in soup.find_all('table'):
		if _rightProp(i,"This layout table holds message information","summary"):
			table=i
			break
	data = {"studentname":table.find('td').find_next('td').contents[0].split(',')[1].strip()}
	data["surname"]= data["studentname"].split(' ')[-1]
	data["givennames"]=" ".join(data["studentname"].split(' ')[:-1])
	return data
