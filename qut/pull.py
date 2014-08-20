from mechanize import Browser

def writeOut(x):
	f=open('out.html',"w+")
	f.write(x)
	f.close
	return x

def auth(username,password):
	browser=Browser()
	browser.set_handle_robots(False)
	browser.open("https://esoe.qut.edu.au/web/enterpriselogin.htm")
	browser.select_form("userpassAuthenticator")
	browser.form["esoeauthn_user"]=username
	browser.form["esoeauthn_pw"]=password
	browser.submit()
	map(browser.open,["https://qutvirtual.qut.edu.au/","https://qutvirtual.qut.edu.au/group/mycampus/home"])#"https://qutvirtual4.qut.edu.au/group/student/home"])# "https://qutvirtual4.qut.edu.au/web/guest", "https://qutvirtual4.qut.edu.au/c/portal/layout", "https://qutvirtual4.qut.edu.au/web/mycampus/home", "https://mccas.qut.edu.au/casshib/shib/mycampus/login?service=https%3A%2F%2Fqutvirtual4.qut.edu.au%2Fc%2Fportal%2Flogin", "https://esoe.qut.edu.au/sso", "https://qutvirtual4.qut.edu.au/group/student/home"])
	browser.select_form("samlRequest")
	browser.submit()
	browser.select_form("samlResponse")
	browser.submit()
	browser.open("https://estudent.qut.edu.au/eStudent/")
	browser.select_form("samlRequest")
	browser.submit()
	browser.select_form("samlResponse")
	browser.submit()
	return browser

def pullClosure(url):
	def closure(browser):
		browser.open(url)
		return browser.response().read()
	return closure

pullMainPage	= pullClosure('https://qutvirtual4.qut.edu.au/group/student/home')
pullTimetable	= pullClosure("https://qutvirtual4.qut.edu.au/group/student/study")
pullEnrollment	= pullClosure("https://estudent.qut.edu.au/eStudent/SM/EnrDtls10.aspx?r=QUT.ESTU.NOCAR.ROLE&f=%24S1.EST.ENRDTLS.WEB")
pullInformation	= pullClosure("https://estudent.qut.edu.au/eStudent/SM/CntctDtls10.aspx?r=QUT.ESTU.NOCAR.ROLE&f=%24S1.EST.CTCTDTL.WEB")
