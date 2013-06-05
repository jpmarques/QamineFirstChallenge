var http = new XMLHttpRequest();
http.open("GET", "/challenge", false);
http.send(null);

parts = http.responseText.split('\n')[0].split(' ')

a = parseInt(parts[5])
b = parseInt(parts[7])

if (parts[4] == 'subtract') result = b-a
if (parts[4] == 'add') result = a+b
if (parts[4] == 'divide') result = a/b
if (parts[4] == 'multiply') result = a*b

result = parseInt(result)

params = 'contact=<email.address>&payload='+result+'&id='+parts[15]

http.open('POST', '/answer', true);
http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
http.send(params);

http.onreadystatechange = function() {
	if(http.readyState == 4 && http.status == 200) {
		console.log(http.responseText);
	}
}
