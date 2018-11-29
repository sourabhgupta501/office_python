import requests, pandas, re, string
#from requests import Request, Session
from bs4 import BeautifulSoup

auth = requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008')

def transport_ext(soup):

    try:
        for table_tag in soup.findAll('table'):
            if 'Transport Type:' in table_tag.text :
                trasport_type = table_tag.text
                break
        trasport_type
    except :
        print('transport comment not found')
        return ''
    return trasport_type   

def hyperlink_ext(soup):
    try:    
        for list_tag in soup.findAll('li'):
            if 'ACTUALS LINK .......' in list_tag.text:
                url = 'http://polldslam/cgi-bin/QC/DSL/' + list_tag.find('a')['href']
                break
        url
    except :
        print('url not found')
        return ''
    return url


def up_down_speed(url):
    resp = requests.get(url=url, auth=auth)
    soup = BeautifulSoup(resp.content, 'html5lib')
    #print(soup.prettify)

    try:
	
        for table_tag in soup.findAll('table'):
            if 'SIGNAL QUALITY STATISTICS' in table_tag.text:
                speed = extract_speed(table_tag)
#                return speed[0], speed[1]

        for table_tag in soup.findAll('table'):
            if 'FULL DATA RATE' in table_tag.text:
                speed = extract_speed(table_tag)
        speed[0]
        speed[1]
        return speed[0], speed[1]
    except:        
        return '', ''

def extract_speed(table_tag):
    speed = []
    for td_tag in table_tag.findAll('td'):
        if bool(re.search("\d.*\s\/\s\d*", td_tag.text)):
            print(td_tag.text)
            b = re.sub("\(.*\)", "", td_tag.text)
            a = td_tag.find('table')
            if a == None:
                speed.append(b)
            else:
                speed.append(b.replace(a.text, ''))
    return speed

if __name__ == "__main__":
   
    df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\PC360_Mobile_APP_.csv", sep = ",")
    i = 0

    for num in df['WTN']:

        url = 'http://polldslam/cgi-bin/QC/DSL/dslam6100Int.pl'
        post_data = {}
        post_data['telephoneNum']=  num
        resp = requests.post(url=url, data= post_data, auth=auth)
        soup = BeautifulSoup(resp.content, 'html5lib')

        df.ix[i, 'Status'] = transport_ext(soup)
        if df.ix[i, 'Status'] == '':
            continue
        print(df.ix[i, 'Status'])
        link = hyperlink_ext(soup)
        if link == '':
            continue
        df.ix[i, 'Up_Speed'], df.ix[i, 'Down_Speed'] = up_down_speed(link)
        print(df.ix[i, 'Up_Speed'])
        print(df.ix[i, 'Down_Speed'])
        i = i+1
        if i > 50:
            break
           # exit()
           
#    df.dropna(inplace = True)
    Up_Speed = df['Up_Speed'].str.split('/', n = 2, expand = True)
    df['UP-Actual'] = Up_Speed[0]
    df['UP-Provisioned'] = Up_Speed[1]
    df['UP-Purchased'] = Up_Speed[2]
#    df['Up-Prov Rate'] = str(pandas.to_numeric(pandas.to_numeric(Up_Speed[0],  errors='coerce')/pandas.to_numeric(Up_Speed[1])*100)) + "% Full Prov Rate"
#    df['Up-Purch Rate'] = str(pandas.to_numeric(pandas.to_numeric(Up_Speed[0],  errors='coerce')/pandas.to_numeric(Up_Speed[2])*100)) + "% Full Purch Rate"
    #    df.drop(columns =['Up_Speed'], inplace = True)
    
    Down_Speed = df['Down_Speed'].str.split('/', n = 2, expand = True)
    df['Down-Actual'] = Down_Speed[0]
    df['Down-Provisioned'] = Down_Speed[1]
    df['Down-Purchased'] = Down_Speed[2]
#    df['Down-Prov Rate'] = str(pandas.to_numeric(pandas.to_numeric(Down_Speed[0],  errors='coerce')/pandas.to_numeric(Down_Speed[1])*100)) + "% Full Prov Rate"
#    df['Down-Purch Rate'] = str(pandas.to_numeric(pandas.to_numeric(Down_Speed[0],  errors='coerce')/pandas.to_numeric(Down_Speed[2])*100)) + "% Full Purch Rate"
    df.drop(columns =['Up_Speed','Down_Speed'], inplace = True)

    df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)
