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
                #print(table_tag.find('th').text)
                speed = extract_speed(table_tag)
                #up_spead = table_tag.findAll('td')[11].text
                #down_spead = table_tag.findAll('td')[21].text
                return speed[0], speed[1]
        for table_tag in soup.findAll('table'):
            if 'SIGNAL QUALITY STATISTICS' in table_tag.text:
                #print(table_tag.find('th').text)
                speed = extract_speed(table_tag)
                #up_spead = table_tag.findAll('td')[11].text
                #down_spead = table_tag.findAll('td')[21].text
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
                #print(b)
                speed.append(b)
            else:
                #print(a)
                speed.append(b.replace(a.text, ''))
    return speed
                         
##            a = re.findall("<table.*?<\/table>", td_tag)
##            speed.append(re.findall("\d.*\s\/\s\d*", td_tag.text))

##    #return speed
##a = '''<table border="3" cellpadding="1" cellspacing="1"><tbody><tr><th align="center" bgcolor="FFFFB0" colspan="6"><font face="Arial" size="+1">SIGNAL QUALITY STATISTICS</font></th></tr><tr align="center"><td></td><td width="50"><font face="Arial" size="-1"><b>Output<br/>Power<br/><font face="Consolas">(dB)</font></b></font></td><td width="50"><font face="Arial" size="-1"><b>Noise<br/>Margin<br/><font face="Consolas">(dB)</font></b></font></td><td width="50"><font face="Arial" size="-1"><b>Atten<br/><font face="Consolas">(dB)</font></b></font></td><td width="50"><font face="Arial" size="-1"><b>Delay<br/><font face="Consolas">(ms)</font></b></font></td><td><font face="Arial" size="-1"><b>Data Rate</b><br/><font style="font-size:80%;"><i>(<b>Actual</b> </i>/<i> <font color="#0000CC">Prov</font> </i>/<i> <font color="#006600">Purch</font>)</i><br/></font><font face="Consolas"><b>(kbps)</b></font></font></td></tr><tr align="center"><td><font face="Arial" size="-1"><b>Upstream</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b> / <font color="#0000CC">5120</font> / <font color="#006600">5120</font><br/><font color="#222222" style="font-size:8pt;">(Max Attainable = 0)</font></font></td></tr><tr align="center"><td><font face="Arial" size="-1"><b>Downstream</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b></font></td><td><font face="Arial" size="-1"><b>0</b> / <font color="#0000CC">20128</font> / <font color="#006600">20128</font><br/><font color="#222222" style="font-size:8pt;">(Max Attainable = 0)</font></font></td></tr></tbody></table>'''
##soup = BeautifulSoup(a, 'html5lib')
##extract_speed(a)
####
#print(up_down_speed("http://polldslam/cgi-bin/QC/DSL/adtranActuals.pl?telephoneNum=3033719936&ip=10.228.142.162&shelf=3&slot=1&port=30&ac=1&isTA5000=0&isTA3000=0&vcString=&LC=Q&tDR=10.228.142.162&isIPTV=0&isIPME=0&orderedSpeed=5120K/20128K"))    
#print(up_down_speed("http://polldslam/cgi-bin/QC/DSL/calixActuals.pl?telephoneNum=7855942300&ip=10.65.238.172&slot=1&port=9&port2=10&telephoneNum2=7855942300&ac=1&LC=C&tDR=10.65.238.172&isIPTV=&orderedSpeed=2000K/25000K"))




    
df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\Bieser_Team_PC360_use-2018-10-25.csv", sep = ",")
i = 0
for num in df['WTN']:
    df.ix[i, 'Status'], url = extract_transort_comment(num)
    print(df.ix[i, 'Status'])
    if url != '':
        df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'] = up_down_speed(url)
        print(df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'])
    i = i+1
df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)
