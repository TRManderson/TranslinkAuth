import mechanize

_rotaUserAgent="Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 (.NET CLR 3.5.30729)"
_FINALURL="https://www.sinet.uq.edu.au/psc/ps_4/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_CRSE_HOME.GBL"



def pullPage(username,password):
	browser=mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders=[
		("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0"),
		("Accept-Language","en-US,en")
	]
	map(browser.open,["https://www.sinet.uq.edu.au/","https://www.sinet.uq.edu.au/psp/ps/?cmd=login","https://www.sinet.uq.edu.au/ps/uqsinetsignin.html"])

	browser.select_form("login")
	browser.set_all_readonly(False)
	browser.form["userid1"]=username
	browser.form["pwd"]=password
	browser.form["timezoneOffset"]="-600"
	browser.form["userid"]=username.upper()
	browser.submit()
	browser.open("https://www.sinet.uq.edu.au/psp/ps/EMPLOYEE/HRMS/h/?tab=UQ_MYPAGE&pageletname=MENU&cmd=refreshPglt")
	browser.open(_FINALURL)
	return browser.response().read()
