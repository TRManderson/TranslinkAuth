import webapp2
import uq
import gr
import qut
import pypdftk
from collections import namedtuple
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
		pdfData["Text17"]=now.day
		pdfData["Text18"]=now.month
		pdfData["Text19"]=now.year
	except Exception:
		pass
	newfile=pypdftk.fill_form("./new.pdf",pdfData)
	f=open(newfile,"rb")
	return f