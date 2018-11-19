
import requests

from bs4 import BeautifulSoup

session_requests = requests.session()

login_url = "http://ssowp01/AgPM/Default.aspx?status=0"


headers = {'User-Agent':
          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
          }

login_data = { '__EVENTTARGET':'', 
               '__EVENTARGUMENT':'', 
               '__VIEWSTATE': '/wEPDwULLTEyNDQzMTk3NzBkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtpbWdCdG5Mb2dpbuIqxAMCeybZlgAxHU4tua/KsqPYpSvfp1KJm1vOfTxK',
               '__VIEWSTATEGENERATOR': '7945D3DC',
               '__EVENTVALIDATION': '/wEdAAVwR9nwHeFblMlDs2uuUT+kY3plgk0YBAefRz3MyBlTcHY2+Mc6SrnAqio3oCKbxYbZSBEyYVEUHTBPdIEnjDeERX2g4gLGtWIyn+8EDY/rCtarjgjH0X+PlGCZ42BoCwQIaFBQ/vdHnYJ6Hl/cFCPx',
               'txtUserName': 'AB73171',
               'txtPassword': 'Ctli@008',
               'imgBtnLogin.x': '0',
               'imgBtnLogin.y': '0'

    }
result = session_requests.get(login_url, headers= headers)

# To find the dynamic dat in login_data

#soup = Beautifulsoup(result.content, 'html5lib')
#login_data['__VIEWSTATE'] = soup.find

result = session_requests.post(login_url,data= login_data, headers= headers)
print(result.url)

soup = BeautifulSoup(result.content, 'html5lib')

with open("output1.html", "w") as file:
    file.write(str(soup.prettify()))

file.close()
