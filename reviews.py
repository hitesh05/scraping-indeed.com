from time import sleep
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import csv
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

S=Service(ChromeDriverManager().install())
DRIVER = webdriver.Chrome(service=S)

NO_OF_PAGES = 100
START = 32166
END = 34277

filename1 = 'reviews1.csv'
filename2 = 'reviews2.csv'
filename3 = 'reviews3.csv'
filename4 = 'reviews4.csv'

def get_links(names):
    links = []
    l = 'http://www.indeed.com/cmp/'
    for i in names:
        i = i[2:-2]
        i = re.sub('\s','-',i)
        i = re.sub('.com','',i)
        i = re.sub('[0-9]','',i)
        i = re.sub(',','',i)
        i = l+i
        links.append(i)
        
    unique_list = []
    for x in links:
        if x not in unique_list:
            unique_list.append(x)
        
    return unique_list


def get_soup(l):
    l += "/reviews?start="  
    ans = []  
    for i in range(0,NO_OF_PAGES):
        page = i
        link = (
            l
            + str(page*20)
        )
        # print(link)
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            ans.append(soup)
        except:
            return ans
        
        try:     
            n = soup.find_all('a', class_='css-3iy1zx e8ju0x50')[-1].get_text()
        except:
            return ans
        if n.lower() != "next":
            return ans
        
    return ans

def review(ans):
    reviews = []
    for x in ans:
        try:
            a = x.find_all('a',class_='css-i1omlj emf9s7v0')
            b = x.find_all(
                "div",
                attrs={
                    "data-tn-component": "reviewDescription",
                    "class": "css-rr5fiy eu4oa1w0"
                },
            )
            c = x.find_all('button', class_='css-1c33izo e1wnkr790')
        except:
            continue
        for i in range(len(a)):
            r = c[i].get_text() + " stars. " + a[i].get_text() + b[i].get_text()
            reviews.append(r)
            
    return reviews

data = pd.read_csv('../out_final.csv', sep=',', on_bad_lines='skip')
names = data['Company Name']
# links = get_links(names)
# data = pd.read_csv('out_final2.csv', sep=',', on_bad_lines='skip')
# names2 = data['Company Name']
# names3 = []
# for i in names:
#     names3.append(i)
# for i in names2:
#     names3.append(i)
# print(len(names3))
links = get_links(names)
# print(len(links))
# quit()

for i, link in enumerate(links):
    if i >= START and i < END:
        ans = get_soup(link)
        reviews = review(ans)
        row = []
        row.append(link[26:])
        for r in reviews:
            row.append(r)
        if len(row)<= 100:
            with open(filename1,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))
        elif len(row) > 100 and len(row)<=500:
            with open(filename2,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))
        elif len(row)>500 and len(row)<=1000:
            with open(filename3,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))
        else:
            with open(filename4,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))
        print('here', i)
        