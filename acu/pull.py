from mechanize import Browser
from common import pullClosure,writeOut

def auth(username,password):
	browser=Browser()
	browser.set_handle_robots(False)
	browser.open("https://www.studentconnect2008.acu.edu.au/ban8/twbkwbis.P_ValLogin")
	browser.select_form('loginform')
	browser.form["sid"]=username.upper()
	browser.form["PIN"]=password
	browser.submit()
	return browser

testuser=auth()

pullInformation=pullClosure("https://www.studentconnect2008.acu.edu.au/ban8/bwgkogad.P_SelectAtypUpdate")
#writeOut(pullInformation(testuser))

def pullEnrollment(browser):
	browser.open("https://www.studentconnect2008.acu.edu.au/ban8/bwckcoms.P_StoreStudyPath")
	writeOut(browser.response().read())
	print browser.geturl

#pullEnrollment(testuser)

#print writeOut(testuser.response().read())