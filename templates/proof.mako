<%include file="header.mako"/>
	<div class="jumbotron"><div class="container text-center">
	<p>This student is...</p>
	<h1>TTCC
	% if eligible:
		Eligible
	% else:
		Ineligible
	% endif
	</h1>
	% if hours >= 12:
		% if enrollment=="Full Time":
			<p>They are considered a full time student and attend 12 or more contact hours a week</p>
		% else:
			<p>They attend 12 or more contact hours a week</p>
		%endif
	% elif enrollment=="Full Time":
			<p>They are considered a full time student</p>
	%endif
	<div class="text-left">
	<dl>
	<dt>Student Name</dt>
	<dd>${studentname}</dd>
	<dt>Student Number</dt>
	<dd>${studentno}</dd>
	<dt>Enrollment Status</dt>
	<dd>${enrollment}</dd>
	</dl></div>
	<div class="text-left">
	<table class="table">
	<thead>
		<td>Course Code</td>
		<td>Course Title</td>
		<td>Hours per Week</td>
	</thead>
	% for course in courselist:
	<tr>
		<td>${course.code}</td>
		<td>${course.title}</td>
		<td>${course.hours}</td>
	</tr>
	%endfor
	</table></div>
	</div></div>
<%include file="footer.mako"/>