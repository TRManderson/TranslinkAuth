<%include file="header.mako"/>
	<h1>No TTCC.</h1>
	<p>Fill out your login details, click a button, and wait patiently. You know how slow logging in is for you, it's just as slow for another computer.</p>
	${extradetails}
	<form role="form" method="POST" action="${suburl}">
		<div class="form-group">
		<input type="text" name="username" placeholder="Username" value="${usr}"/>
		</div>
		<div class="form-group ${{True:"has-warning",False:""}[incorrect]}">
		<input type="password" name="password" placeholder="Password" />
		</div>
		<div class="form-group">
		<input type="submit" onClick="this.form.action='${suburl}';this.form.submit()" class="btn btn-default" name="btn" value="Prove Yourself!" />
		</div>
		<div class="form-group">
		<input type="button" onClick="this.form.action='${suburl}/ttcc.pdf';this.form.submit()" class="btn btn-default" name="btn" value="Get a TTCC Form" />
		</div>
	</form>
	${extra}
<%include file="footer.mako"/>