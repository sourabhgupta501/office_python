import requests
from bs4 import BeautifulSoup

def ext_q_link(soup):    
    links = soup.findAll('a')
    Quiz_links = {}

    for link in links:
        if len(link.getText())<8 and link.getText()[:5]=='Quiz ' :
            Quiz_links[link.getText()] = link.get('href')
    return Quiz_links

def ext_a_link(link_dic):
    
    Sol_links = {}
    for key, value in link_dic.items():        
        result = requests.get(value)
        soup = BeautifulSoup(result.content, 'html5lib')  
        links = soup.findAll('a')
        a = ['CLICK HERE FOR THE ANSWERS', 'English Questions For IBPS PO and Clerk Exam 2017', 'Check Detailed Solutions of English Language']
        for link in links:
            if any(x in link.getText() for x in a):
                Sol_links[key + " Solution"] = link.get('href')
    return Sol_links

def ext_Q_A(link_dic, div_id):
    for key, value in link_dic.items():        
        result = requests.get(value)
        soup = BeautifulSoup(result.content, 'html5lib')  
        with open(key+".txt", "w") as file:
            file.write(soup.find('div',id = div_id).getText())
            file.close()


result = requests.get('https://www.bankersadda.com/p/english-new-pattern.html')
#page = requests.request('http://pythonprogramming.net')

soup = BeautifulSoup(result.content, 'html5lib')
Quiz_links = ext_q_link(soup)

#[ print(key+ ' = '+ value + '\n') for key, value in Quiz_links.items()]


Sol_links = ext_a_link(Quiz_links)
#ext_Q_A(Sol_links, 'PostBody')

[ print(key+ ' = '+ value + '\n') for key, value in Sol_links.items()]

