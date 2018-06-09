import requests
url = 'https://www.ttrar.com/.svn/entries'
res = requests.get(url, timeout=10)
contentType = res.headers['Content-Type']
print(contentType)