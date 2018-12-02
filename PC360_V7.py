import threading
from queue import Queue
import time

import requests, pandas, re, string
#from requests import Request, Session
from bs4 import BeautifulSoup

auth = requests.auth.HTTPBasicAuth('AB73171', 'Ctli@008')


'''   **************************************
      **************************************
      
      Used in 'main_fun' function only
        
      **************************************
      **************************************
'''


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



def Cal_rate(df, num_rator, denom_rator, new_col_name, str_add):
    re_list = []
    i = 0
    for x in df[num_rator]:
        if pandas.isna(x):
            df.ix[i, new_col_name] = ''
            i = i+1
            continue
        elif bool(re.search("\d+", x)) and int(x)>0:
            df.ix[i, new_col_name] = str(int(int(x)/int(df.ix[i, denom_rator])*100)) + str_add
        else:
            df.ix[i, new_col_name] = ''
            i = i+1
            continue
        i = i+1
    return df


'''   **************************************
      **************************************
      
      Used in 'up_down_speed' function only
        
      **************************************
      **************************************
'''
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

                    
def test2():
    print(0)



def main_fun(df):
   
#    df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\PC360_Mobile_APP_.csv", sep = ",")
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
        if i > 2:
            break
           # exit()
           
    Up_Speed = df['Up_Speed'].str.split('/', n = 2, expand = True)
    Up_Speed.fillna('')
    df['UP-Actual'] = Up_Speed[0]
    df['UP-Provisioned'] = Up_Speed[1]
    df['UP-Purchased'] = Up_Speed[2]
#    df.fillna('')       
    df = Cal_rate(df, 'UP-Actual', 'UP-Provisioned', 'Up-Prov Rate','% Full Prov Rate' )
    df = Cal_rate(df, 'UP-Actual', 'UP-Purchased', 'Up-Purch Rate','% Full Purch Rate' )
    
#    df['Up-Prov Rate'] = str(pandas.to_numeric(pandas.to_numeric(Up_Speed[0],  errors='coerce')/pandas.to_numeric(Up_Speed[1])*100, errors='coerce', downcast='integer'))+ "% Full Prov Rate"
#    df['Up-Purch Rate'] = str(pandas.to_numeric(pandas.to_numeric(Up_Speed[0],  errors='coerce')/pandas.to_numeric(Up_Speed[2])*100, errors='coerce', downcast='integer')) + "% Full Purch Rate"
    
    Down_Speed = df['Down_Speed'].str.split('/', n = 2, expand = True)
    Down_Speed.fillna('')
    df['Down-Actual'] = Down_Speed[0]
    df['Down-Provisioned'] = Down_Speed[1]
    df['Down-Purchased'] = Down_Speed[2]
    df = Cal_rate(df, 'Down-Actual', 'Down-Provisioned', 'Down-Prov Rate','% Full Prov Rate' )
    df = Cal_rate(df, 'Down-Actual', 'Down-Purchased', 'Down-Purch Rate','% Full Purch Rate' )

#    df['Down-Prov Rate'] = str(pandas.to_numeric(pandas.to_numeric(Down_Speed[0],  errors='coerce')/pandas.to_numeric(Down_Speed[1])*100, errors='coerce', downcast='integer'))+ "% Full Prov Rate"
#    df['Down-Purch Rate'] = str(pandas.to_numeric(pandas.to_numeric(Down_Speed[0],  errors='coerce')/pandas.to_numeric(Down_Speed[2])*100, errors='coerce', downcast='integer')) + "% Full Purch Rate"

    df.drop(columns =['Up_Speed','Down_Speed'], inplace = True)

#    df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)
    return df


def split_dataframe_to_chunks(df, n):
    df_len = len(df)
    count = 0
    dfs = []

    while True:
        if count > df_len-1:
            break

        start = count
        count += n
        #print("%s : %s" % (start, count))
        dfs.append(df.iloc[start : count])
    return dfs


def threader():
    while True:
        # gets an worker from the queue
        df = q.get()

        # Run the example job with the avail worker in queue (thread)
        main_fun(df)

        # completed with the job
        q.task_done()



if __name__ == "__main__":
    df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\PC360 - Copy.csv", sep = ",")
    list_df = split_dataframe_to_chunks(df, 8)
    
    q = Queue()
    
    # how many threads are we going to allow for
    for x in range(10):
         t = threading.Thread(target=threader)

         # classifying as a daemon, so they will die when the main dies
         t.daemon = True

         # begins, must come after daemon definition
         t.start()

    start = time.time()

    #  jobs assigned.
    for df in list_df:
        q.put(df)

    # wait until the thread terminates.
    q.join()
    
    df = pandas.concat(list_df, axis=0)
    df.to_csv('PC360.csv', sep=',', encoding='utf-8', index=False)


    # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
    # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
    print('Entire job took:',time.time() - start)

