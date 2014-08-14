<%include file="header.mako"/>
<div class="jumbotron"><div class="container text-center">
	<h1>Translink Auth</h1>
	<p>Prove to Translink you're a full time student
	and get a filled-out TTCC application if you've been lazy so far!</p>

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