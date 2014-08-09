def proof(*args,**kwargs):
	x="""<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>"""
	x+=kwargs["title"]
	x+="""</title>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
	<style type="text/css">
		body{background-color: #240330;}
	</style>
	<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body>
	<div class="jumbotron"><div class="container text-center">
	<h1>TTCC """
	if kwargs["eligible"]:
		x+="Eligible"
	else:
		x+="Ineligible"
	x+="""</h1>
	<div>
	<dl>
	<dt>Student Name</dt>
	<dd>"""+kwargs["studentname"]+"""</dd>
	<dt>Student Number</dt>
	<dd>"""+kwargs["studentno"]+"""
	<dt>Enrollment Status</dt>
	<dd>"""+kwargs["enrollment"]+"""
	</dl></div>
	<div>
	<table>
	<thead>
		<td>Course Code</td>
		<td>Course Title</td>
		<td>Hours per Week</td>
	</thead>"""
	for course in kwargs["courselist"]:
		x+="""
	<tr>
		<td>"""+str(course.code)+"""</td>
		<td>"""+str(course.title)+"""</td>
		<td>"""+str(course.hours)+"""</td>
	</tr>"""
	x+="""
	</table></div>
	</div></div>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
</body>
</html>"""
	return x


def landing(*args, **kwargs):
	return """<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>"""+str(kwargs["title"])+"""</title>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
	<style type="text/css">
		body{background-color: #240330;}
	</style>
	<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
<body>
<div class="jumbotron"><div class="container text-center">
	<h1>Translink Auth</h1>
	<p>Prove to Translink you're a full time student,
	and get a filled-out TTCC application while you're at it</p>

	<form role="form" method="POST" action="/">
		<div class="form-grounp">
		<input type="text" name="username" placeholder="Username" />
		</div>
		<div class="form-grounp">
		<input type="password" name="password" placeholder="Password" />
		</div>
		<div class="form-grounp">
		<input type="submit" class="btn btn-default" value="Prove Yourself!" />
		</div>
		<!--<div class="form-grounp">
		<input type="submit" class="btn btn-default"TTCC Application</button>
		</div>-->
	</form>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
</div></div>
</body>
</html>
"""