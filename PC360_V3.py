import requests, pandas
#from requests import Request, Session
from bs4 import BeautifulSoup

auth = requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008')

def extract_data(num):
    
    url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Int.pl'
    post_data = {}
    post_data['telephoneNum']=  num
    resp = requests.post(url=url, data= post_data, auth=auth)
    soup = BeautifulSoup(resp.content, 'html5lib')

    try:
        for table_tag in soup.findAll('table'):
            if 'Transport Type:' in table_tag.text :
                trasport_type = table_tag.text
                break
        print(trasport_type)
    except :
        print('transport comment not found')
        return '', '', ''
    
    try:    
        for list_tag in soup.findAll('li'):
            if 'ACTUALS LINK .......' in list_tag.text:
                url_part = 'http://polldslam/cgi-bin/QC/DSL/' + list_tag.find('a')['href']
                break
        print(url_part)
    except :
        print('url not found')
        return trasport_type , '', ''

    resp = requests.get(url=url_part, auth=auth)
    soup = BeautifulSoup(resp.content, 'html5lib')

    try:
        for table_tag in soup.findAll('table'):
           # print(table_tag.find('th'))
            if 'FULL DATA RATE' in table_tag.text:
                print(table_tag.find('th').text)
                up_spead = table_tag.findAll('td')[11].text
                down_spead = table_tag.findAll('td')[21].text
                return trasport_type, url_part, down_spead
        for table_tag in soup.findAll('table'):
            if 'SIGNAL QUALITY STATISTICS' in table_tag.text:
                print(table_tag.find('th').text)
                up_spead = table_tag.findAll('td')[11].text
                down_spead = table_tag.findAll('td')[21].text
                return trasport_type, up_spead, down_spead
    except:        
        return trasport_type, up_spead, up_spead


df = pandas.read_csv(r"C:\Users\AB73171\Desktop\Data_Saurav\PC 360\Bieser_Team_PC360_use-2018-10-25.csv", sep = ",")
i = 0
for num in df['WTN']:
    df.ix[i, 'Status'], df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'] = extract_data(num)
    i = i+1
df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)
