import requests, pandas, re, string
#from requests import Request, Session
from bs4 import BeautifulSoup

auth = requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008')

def extract_transort_comment(num):
    
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
        trasport_type
    except :
        print('transport comment not found')
        return '', ''
    
    try:    
        for list_tag in soup.findAll('li'):
            if 'ACTUALS LINK .......' in list_tag.text:
                url_part = 'http://polldslam/cgi-bin/QC/DSL/' + list_tag.find('a')['href']
                break
        url_part
    except :
        print('url not found')
        return trasport_type , ''
    return trasport_type , url_part

def up_down_speed(url):
    resp = requests.get(url=url, auth=auth)
    soup = BeautifulSoup(resp.content, 'html5lib')

    try:
        for table_tag in soup.findAll('table'):
            if 'FULL DATA RATE' in table_tag.text:
                 speed = extract_speed(table_tag)
                 return speed[0], speed[1]
        for table_tag in soup.findAll('table'):
            if 'SIGNAL QUALITY STATISTICS' in table_tag.text:
                speed = extract_speed(table_tag)
                return speed[0], speed[1]
    except:        
        return '', ''

def extract_speed(table_tag):
    speed = []
    for td_tag in table_tag.findAll('td'):
         if bool(re.search("\d.*\s\/\s\d*", td_tag.text)):
            b = re.sub("\(.*\)", "", td_tag.text)
            a = td_tag.find('table')
            if a == None:
                speed.append(b)
            else:
                speed.append(b.replace(a.text, ''))
    return speed
    
df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\PC360_Mobile_APP_.csv", sep = ",")
i = 0
for num in df['WTN']:
    df.ix[i, 'Status'], url = extract_transort_comment(num)
    print(df.ix[i, 'Status'])
    if url != '':
        df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'] = up_down_speed(url)
##        Up_Speed, Down_Speed = up_down_speed(url)
##        df.ix[i, 'UP-Actual'], df.ix[i, 'UP-Provisioned'], df.ix[i, 'UP-Purchased'] = Up_Speed.split('/')
##        df.ix[i, 'UP Prov Rate'] = int(int(Up_Speed.split('/')[0])/int(Up_Speed.split('/')[1])*100)
##        df.ix[i, 'UP Purch Rate'] = int(int(Up_Speed.split('/')[1])/int(Up_Speed.split('/')[2])*100)
##        
##        df.ix[i, 'Down-Actual'], df.ix[i, 'Down-Provisioned'], df.ix[i, 'Down-Purchased'] = Down_Speed.split('/')
##        df.ix[i, 'Down Prov Rate'] = int(int(Down_Speed.split('/')[0])/int(Down_Speed.split('/')[1])*100)
##        df.ix[i, 'Down Purch Rate'] = int(int(Down_Speed.split('/')[1])/int(Down_Speed.split('/')[2])*100)
        
    i = i+1
df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)
