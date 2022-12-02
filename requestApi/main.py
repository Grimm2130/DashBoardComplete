from subprocess import list2cmdline
import urllib.request as url
import ssl
import json
from pprint import pprint

myUrl = "https://localhost:7072/api/Wine"
context = ssl._create_unverified_context()
myRequest = url.urlopen(myUrl, context=context)


print("MY request code: " + str(myRequest.getcode()))

data = myRequest.read()
data= json.loads(data)
# data = data.
for i in data:
    print(i)