import requests
from requests import Request, Session
from bs4 import BeautifulSoup


url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Int.pl'
s = Session()

login_data = { 'telephoneNum': '3033670025'}
req = Request('POST', url, auth=requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008'), data= login_data)

prepped = s.prepare_request(req)

# Merge environment settings into session
#settings = s.merge_environment_settings(prepped.url, None, None, None, None)
#resp = s.send(prepped, **settings)

resp = s.send(prepped)

soup = BeautifulSoup(resp.content, 'html5lib')

print(soup.findAll('font', face = "Arial")[13].text)

print(resp.status_code)

links = soup.findAll('a')

for link in links:
    if link.text == 'Adtran DSLAM Actuals':
        url_part = link['href']

#'http://polldslam/cgi-bin/QC/DSL' + url_part
print('http://polldslam/cgi-bin/QC/DSL/' + url_part)

req = Request('GET', 'http://polldslam/cgi-bin/QC/DSL/' + url_part, auth=requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008'))
prepped = s.prepare_request(req)
resp = s.send(prepped)
soup = BeautifulSoup(resp.content, 'html5lib')
#print(soup.text)

print(soup.findAll('table', border="3")[2].text)
print(soup.find('th').text)

soup = soup.findAll('table', border="3")[2]
print(soup.findAll('td')[11].text)
print(soup.findAll('td')[17].text)


##
##from requests.auth import HTTPBasicAuth
##auth = HTTPBasicAuth('AB73171', 'Ctli@008')
##
##r = requests.post(url=url, data=body, auth=auth)
##r.status_code
##201
##
##content = r.json()
##print(content[u'body'])
