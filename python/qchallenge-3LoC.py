import httplib, urllib, re, operator

r = urllib.urlopen('http://engineer.qamine.com/challenge').read()
result = eval(''.join(r.replace('to', '+').replace('by', '/').replace('times', '*').replace('subtract ', ' -').split(' ')[5:8]))
print urllib.urlopen('http://engineer.qamine.com/answer', 'contact=jp.mrqs%40gmail.com&payload=' + str(result) +'&id=' + r.split('\n')[0].split(' ')[15]).read()
