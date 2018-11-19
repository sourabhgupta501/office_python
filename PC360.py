##import urllib3
##
##
##x = urllib3.PoolManager().request('GET', 'http://polldslam/')
##
##print(x.data)

import requests
page = requests.get('http://polldslam/cgi-bin/QC/DSL/dslam6100Form.pl', auth=requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008'))
#page = requests.request('http://pythonprogramming.net')
contents = page.content

