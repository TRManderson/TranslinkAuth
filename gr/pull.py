from mechanize import Browser

def writeOut(x):
	f=open('out.html',"w+")
	f.write(x)
	return f.close

def auth(username,password):
	browser=Browser()
	browser.set_handle_robots(False)
	browser.open("https://auth.griffith.edu.au/pf/adapter2adapter.ping?SpSessionAuthnAdapterId=portal&TargetResource=https%3A%2F%2Fportal.secure.griffith.edu.au%2Fpsp%2FGP90PD%2FGUINTRA%2FGP%2Fh%2F%3Ftab%3DDEFAULT")
	browser.select_form("login")
	browser.form["pf.username"]=username
	browser.form["pf.pass"]=password
	browser.submit()
	return browser

def pullClosure(url):
	def closure(browser):
		browser.open(url)
		return browser.response().read()
	return closure

pullTimetable=pullClosure("https://ps-he.secure.griffith.edu.au/psc/HE90PD/GUINTRA/HE/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL")
pullInformation=pullClosure("https://ps-he.secure.griffith.edu.au/psc/HE90PD/GUINTRA/HE/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL")