import httplib, urllib, re, operator

operationDic = {"subtract": operator.sub, "add": operator.add, "divide": operator.div, "multiply": operator.mul}

# GET
http = urllib.urlopen("http://engineer.qamine.com/challenge")
response = http.read()

numbers = re.findall(r"\d+", response.split("\n")[0]) # find all numbers
numbers = map(lambda x : int(x), numbers) # convert them to int

operationType = response.split(" ")[4]

result = reduce(operationDic[operationType], numbers[:-1]) # apply operation to all number except the last one (id)

# POST
params = urllib.urlencode({'contact':'<>', 'payload': str(result), 'id': str(numbers[-1])})
http = urllib.urlopen("http://engineer.qamine.com/answer", params)
response = http.read()
print response