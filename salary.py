#!/usr/bin/env python3
from time import sleep
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import csv
from datetime import date
from csv import writer
from csv import reader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

S=Service(ChromeDriverManager().install())
DRIVER = webdriver.Chrome(service=S)

filename = 'jobs_updated.csv'

def get_links(names,locations,c_names):
    links = []
    for i in range(len(names)):
        name = names[i]
        location = locations[i]
        c_name = c_names[i]
        
        name = re.sub('\s','%20', name)
        name = re.sub(',','',name)
        location = re.sub('\s','%20', location)
        location = re.sub(',','',location)
        c_name = re.sub('\s','%20', str(c_name))
        c_name = re.sub(',','',c_name)
        
        link = (
            "https://www.indeed.com/jobs?q="
            + name
            + "%20"
            + c_name
            + "&l="
            + location
        )
        # print(link)
        links.append(link)
            
    return links
            
def get_salary(url):
    try:
        DRIVER.get(url)
        # r = requests.get(url)
        # soup = BeautifulSoup(r.content, "html5lib")
    except:
        return ''
    
    try:
        # salary = soup.find_all('ul', class_='css-1lyr5hv eu4oa1w0').get_text()
        # s = DRIVER.find_element(By.CLASS_NAME,"css-1lyr5hv eu4oa1w0")
        s = DRIVER.find_element(By.CLASS_NAME,"resultContent")
        # print(s)
        salary = s.text
    except:
        salary = ''
        
    return salary
    
# url = 'https://www.indeed.com/viewjob?jk=0516478781fddd2e&from=serp&vjs=3'
# url = 'https://www.indeed.com/jobs?q=Learning%20%20Development%20Manager%20Infinitive%20Inc&l=Ashburn%2C%20VA'  
# r = requests.get(url)
# print(r)

# S=Service(ChromeDriverManager().install())
# DRIVER = webdriver.Chrome(service=S)
# DRIVER.get(url)
# salary = get_salary(url)
# salary = salary.lower()
# i1 = salary.split('$', 0)
# i2 = salary.split('K')
# print(salary)
# quit()   

data = pd.read_csv('jobs.csv')
# links = []

names = data['jobtitle']
locations = data['location']
c_names = data['companyname']
des = data['description']
company_link = data['company_link']
job_id = data['job_id']
sal = data['salary']
crawl_date = data['crawl_date']
remote = data['remote']
apply_comp = data['apply_comp']
# salaries = []
# print('here1')
links = get_links(names,locations,c_names) 

fields = ['jobtitle','location','companyname','description','company_link','job_id','salary','crawl_date','remote','apply_comp','salary3']
with open(filename,'w') as file:
    writer = csv.writer(file)
    writer.writerow(fields)
            
            
for i,link in enumerate(links):
    salary = get_salary(link)
    # salaries.append(salary)
    # print(salary)
    row = [names[i],locations[i],c_names[i],des[i],company_link[i],job_id[i],sal[i], crawl_date[i],remote[i], apply_comp[i],salary]
    print('here',i)
    with open(filename,'a') as file:
        writer = csv.writer(file)
        writer.writerow(map(lambda x: [x], row))
    
       
