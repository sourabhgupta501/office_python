import requests, pandas, re, string
#from requests import Request, Session
from bs4 import BeautifulSoup

auth = requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008')


post_data = {}
post_data['telephoneNum']=  '9135922900'


url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Int.pl'
resp = requests.post(url=url, data= post_data, auth=auth)
soup = BeautifulSoup(resp.content, 'html5lib')
