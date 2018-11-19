import pandas as pd
import requests
from bs4 import BeautifulSoup

def ext_q_link(soup):    
    links = soup.findAll('a')
    Quiz_links = {}
    i = 1
    for link in links:
        if len(link.getText())<8 and link.getText()[:5]=='Quiz ' :
            Quiz_links['Quiz'+ str(i)] = link.get('href')
        i = i+1    
    return Quiz_links


topic_links = pd.read_csv("Quiz_links.csv",",")
j = 0
for link in topic_links["Link"]:
    result = requests.get(link)
    soup = BeautifulSoup(result.content, 'html5lib')
    Quiz_links = ext_q_link(soup)
    print(topic_links.ix[j,'Sub-Subject'] + "=" + link)
    #print(Quiz_links)
    file = open(topic_links.ix[j,'Sub-Subject']+".txt", "w")
    for key, value in Quiz_links.items():
            file.write(key + "=" + value + '\n')
    file.close()       

    j = j+1

    if j >3:
        exit()
