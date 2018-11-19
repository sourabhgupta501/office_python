import time
import threading
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
#        return '', ''
    
    try:    
        for list_tag in soup.findAll('li'):
            if 'ACTUALS LINK .......' in list_tag.text:
                url_part = 'http://polldslam/cgi-bin/QC/DSL/' + list_tag.find('a')['href']
                break
        url_part
    except :
        print('url not found')
        print(trasport_type)
#        return trasport_type , ''
#    return trasport_type , url_part

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
for i in range(int(df['WTN'].count()/2)+1):
    print(i+i, i+i+1)
    print(df.ix[i+i,'WTN'], df.ix[i+i+1,'WTN'])
    t1= threading.Thread(target=extract_transort_comment, args=(df.ix[i+i,'WTN'],))
    t2= threading.Thread(target=extract_transort_comment, args=(df.ix[i+i+1,'WTN'],))
    t1.start()
    t2.start()        
    t1.join()
    t2.join()

##    df.ix[i, 'Status'], url = extract_transort_comment(df.ix[i,'WTN'])
##    print(df.ix[i, 'Status'])
##    if url != '':
##        df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'] = up_down_speed(url)
    i = i+1


#df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)













