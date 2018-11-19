import requests
from bs4 import BeautifulSoup

url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Form.pl'
session_requests = requests.session()
result = session_requests.get(url, auth=requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008'))
#page = requests.request('http://pythonprogramming.net')

#soup = BeautifulSoup(result.content, 'html5lib')

#price_box = soup.find('input', attrs={'name':'telephoneNum'})
url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Int.pl'
login_data = { 'telephoneNum': '3033670025'}
result = session_requests.post(url,data= login_data)
soup = BeautifulSoup(result.content, 'html5lib')
#print(result.url)
