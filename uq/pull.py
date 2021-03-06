from common import pullClosure
import mechanize

def auth(username,password):
	browser=mechanize.Browser()
	browser.set_handle_robots(False)
	map(browser.open,["https://www.sinet.uq.edu.au/","https://www.sinet.uq.edu.au/psp/ps/?cmd=login","https://www.sinet.uq.edu.au/ps/uqsinetsignin.html"])
	browser.select_form("login")
	browser.set_all_readonly(False)
	browser.form["userid1"]=username
	browser.form["pwd"]=password
	browser.form["timezoneOffset"]="-600"
	browser.form["userid"]=username.upper()
	browser.submit()
	return browser


pullMyPage=pullClosure("https://www.sinet.uq.edu.au/psp/ps/EMPLOYEE/HRMS/h/?tab=UQ_MYPAGE")
pullCourses=pullClosure("https://www.sinet.uq.edu.au/psc/ps_4/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_CRSE_HOME.GBL")
pullTimetable=pullClosure("https://www.sinet.uq.edu.au/psc/ps_2/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_TM_TBL_LIST.GBL?&STRM=6460")
pullStudyLoad=pullClosure("https://www.sinet.uq.edu.au/psc/ps/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_CHG_STDY_LOAD.GBL")
pullAddress=pullClosure("https://www.sinet.uq.edu.au/psc/ps/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_ADDR.GBL")
pullPhone=pullClosure("https://www.sinet.uq.edu.au/psc/ps/EMPLOYEE/HRMS/c/UQMY_STUDENT.UQMY_PERS_PHONE.GBL")