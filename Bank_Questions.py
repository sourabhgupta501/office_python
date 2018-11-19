import requests
from bs4 import BeautifulSoup

result = requests.get('https://www.bankersadda.com/p/english-new-pattern.html')
#page = requests.request('http://pythonprogramming.net')

soup = BeautifulSoup(result.content, 'html5lib')

links = soup.findAll('a')
Quiz_links = {}

for link in links:
    if len(link.getText())<8 and link.getText()[:5]=='Quiz ' :
        Quiz_links[link.getText()] = link.get('href')


#[ print(key+ '='+ value + '\n') for key, value in Quiz_links.items()]

#Extracts all the Question from Quiz pages and saving in text file

##for key, value in Quiz_links.items():        
##    result = requests.get(value)
##    soup = BeautifulSoup(result.content, 'html5lib')  
##    with open(key+".txt", "w") as file:
##        file.write(soup.find('div',id = 'PostBody').text)
##        file.close()


file = open("Question_Dump.txt", "w")

for key, value in Quiz_links.items():        
    result = requests.get(value)
    soup = BeautifulSoup(result.content, 'html5lib')
    all_ques_links = soup.find_all('div',style = 'text-align: justify;')
    for all_ques_link in all_ques_links:
        if all_ques_link.text != '':
            file.write(str(all_ques_link.text))
    print('One Quize Colepted')
##    [str(all_ques_link.text) for all_ques_link in all_ques_links
##    if all_ques_link.text != '']

file.close
     
##result = requests.get(Quiz_links['Quiz 87'])
##soup = BeautifulSoup(result.content, 'html5lib')
##all_ques_links = soup.find_all('div',style = 'text-align: justify;')
##len(all_ques_links)
##[print(all_ques_link.text) for all_ques_link in all_ques_links if all_ques_link.text != '']
