from mechanize import Browser
from common import pullClosure,writeOut
import requests

def authConnect(username,password):
	browser=Browser()
	browser.set_handle_robots(False)
	browser.open("https://www.studentconnect2008.acu.edu.au/ban8/twbkwbis.P_ValLogin")
	browser.select_form('loginform')
	browser.form["sid"]=username.upper()
	browser.form["PIN"]=password
	browser.submit()
	return browser

def authAllocate(username,password):
	return requests.post("https://acututor.acu.edu.au/rest/student/login",{"username":username,"password":password})
	browser=Browser()
	browser.set_handle_robots(False)
	browser.open("https://acututor.acu.edu.au/rest/student/login")
	browser.form=browser.forms().next()
	browser.form.controls[0]._value=username
	browser.form.controls[1]._value=password
	browser.submit()
	return browser

testuser=auth("","")
pullInformation=pullClosure("https://www.studentconnect2008.acu.edu.au/ban8/bwgkogad.P_SelectAtypUpdate")

#writeOut(pullInformation(testuser))
def pullEnrollment(browser):
	browser.open("https://www.studentconnect2008.acu.edu.au/ban8/bwckcoms.P_StoreStudyPath")
	writeOut(browser.response().read())
	print browser.geturl

def pullTimetable(browser):
	print browser.geturl()
	return browser.response().read()

writeOut(pullTimetable(testuser))

#print writeOut(testuser.response().read())
