import os
dora = {'id':'10003', 'name':'Dora Chen','gender':'female',
        'age':32, 'title':'Sales'}

sHtml = """
<html>
<head>
	<title>Employee {name}'s information</title>
</head>
<body>
	<h1>Employee {name}'s Information</h1>
	<hr>
	<table border=1 width="100%">
		<tr>
			<td>ID:</td>
			<td>{id}</td>
			<td>Name:</td>
			<td>{name}</td>
			<td>Age:</td>
			<td>{age}</td>
		</tr>
		<tr>
			<td>Gender:</td>
			<td>{gender}</td>
			<td>Title:</td>
			<td colspan=3>{title}</td>
		</tr>
	</table>
</body>
</html>
"""
f = open('dora.htm','w')
f.write(sHtml.format_map(dora))
f.close()

os.system("explorer dora.htm")