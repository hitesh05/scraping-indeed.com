#!/usr/bin/env python3
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

'''
Company name - DONE
industry - DONE
size: number of employees - DONE
Revenue: total revenue - DONE
Description: the paragraph that describes the company - DONE
Founding date - DONE
Weblink - DONE
CEO_name - DONE
Overall_rating_score: the website lists 4 years of ratings from 2018-2022; you can split this variable into 4 different ones (overall_rating2018, overall_rating2019, etc.) - DONE
Rating_score_worklife: the rating score for worklife balance - DONE
Rating_score_compensation: for compensation and benefit - DONE
Rating_score_security: for job security and advancement - DONE
Rating_score_management: for management - DONE
Rating_score_culture: for culture - DONE
Salary - DONE
Num_Jobs: I only need the aggregated number of jobs by category; just as the salary information field, you can dump the number of jobs posted for each category of jobs into one field (e.g., “management jobs 3; installation jobs 8; inspection jobs; 10, legal jobs 1, … etc.); just take whatever categories created by Indeed data. - DONE

company id
headquarter location - ???
'''

SCRAPED = 0
START = 0
END = 6424
S=Service(ChromeDriverManager().install())
DRIVER = webdriver.Chrome(service=S)

def get_links(names):
    # print('names', len(names))
    # print(names)
    links = []
    l = 'http://www.indeed.com/cmp/'
    for i in names:
        i = i[2:-2]
        i = re.sub('\s','-',i)
        i = re.sub('.com','',i)
        i = re.sub('[0-9]','',i)
        i = re.sub(',','',i)
        if i =='':
    
            continue
        i = l+i
        i+='/'
        links.append(i)
        
    unique_list = []
    for x in links:
        if x not in unique_list:
            unique_list.append(x)
        
    print(len(unique_list))
    return unique_list

def information(url):
    try:
        # r = requests.get(url)
        # soup = BeautifulSoup(r.content, "html5lib")
        DRIVER.get(url)
    except:
        return '','','','','','','','','','','','','','','','','','','',''
    try:
        # name = soup.find(class_ = 'css-17x766f e1wnkr790').get_text()
        name = DRIVER.find_element(By.XPATH, '//div[@class="css-17x766f e1wnkr790"]').text
    except:
        try:
            # name = soup.find(class_ = 'css-86gyd7 e1wnkr790').get_text()
            name = DRIVER.find_element(By.XPATH, '//div[@class="css-86gyd7 e1wnkr790"]').text
        except:
            name = ''  
    try:
        # info = soup.find_all('div', class_='css-1w0iwyp e1wnkr790')
        # founded = info[0].get_text()
        info = DRIVER.find_elements(By.XPATH, '//div[@class="css-1w0iwyp e1wnkr790"]')
        founded = info[0].text
    except:
        founded = ''  
    try:
        description = DRIVER.find_element(By.XPATH, '//div[@class="css-ol244x eu4oa1w0"]').text
    except:
        description = '' 
    try:
        # link = soup.find('a', class_ = 'css-10y32lq emf9s7v0').get('href')
        link = DRIVER.find_element(By.XPATH, '//a[@class="css-10y32lq emf9s7v0"]').get_attribute('href')
    except:
        link = ''    
    try:
        # founder = soup.find('span', class_='css-1w0iwyp e1wnkr790').get_text()
        founder = DRIVER.find_element(By.XPATH, '//span[@class="css-1w0iwyp e1wnkr790"]').text
    except:
        founder = ''
    try:
        # info = soup.find_all('div', class_='css-1w0iwyp e1wnkr790')
        info = DRIVER.find_elements(By.XPATH, '//div[@class="css-1w0iwyp e1wnkr790"]')
        industry = info[-2].text
    except:
        industry = ''
    try:
        # emprev = soup.find_all(class_='css-1k40ovh e1wnkr790')
        # employees = emprev[0].get_text()
        emprev = DRIVER.find_elements(By.XPATH, '//div[@class="css-1k40ovh e1wnkr790"]')
        employees = emprev[0].text
    except:
        employees = ''
    try:
        revenue = emprev[1].text
    except:
        revenue = ''
    try:
        # rating_old = soup.find_all('g', class_='css-a50thi eu4oa1w0')
        rating_old = DRIVER.find_elements(By.XPATH, '//g[@class="css-a50thi eu4oa1w0"]')
        # rating_old = DRIVER.find_element(By.CLASS_NAME, "css-a50thi eu4oa1w0")
        # rating_old = DRIVER.find_elements(By.XPATH, '//div[@class="css-17yrq7y eu4oa1w0"]')
        # rating_old = rating_old_x.find_elements(By.XPATH, '//g[@class="css-a50thi eu4oa1w0"]')
        # print(rating_old)
        l = len(rating_old)
        # print('l',l)
        rating_2021 = ''
        rating_2020 = ''
        rating_2019 = ''
        rating_2018 = ''
        if l==4:
            rating_2018 = rating_old[0].text
            rating_2019 = rating_old[1].text
            rating_2020 = rating_old[2].text
            rating_2021 = rating_old[3].text
        elif l==3:
            rating_2019 = rating_old[0].text
            rating_2020 = rating_old[1].text
            rating_2021 = rating_old[2].text
        elif l==2:
            rating_2020 = rating_old[0].text
            rating_2021 = rating_old[1].text
        elif l==1:
            rating_2021 = rating_old[0].text
    except:
        # print('except')
        rating_2021 = ''
        rating_2020 = ''
        rating_2019 = ''
        rating_2018 = ''
    try:
        # rating_2022 = soup.find('g', class_ ='css-je7s01 eu4oa1w0').get_text()
        rating_2022 = DRIVER.find_element(By.PARTIAL_LINK_TEXT, '//g[@class="css-je7s01 eu4oa1w0"]').text
        # print(rating_2022)
    except:
        # print('except')
        rating_2022 = ''
    try:
        # review_by_cat = soup.find_all(class_='css-1qdoj65 e1wnkr790')
        review_by_cat = DRIVER.find_elements(By.XPATH, '//span[@class="css-1qdoj65 e1wnkr790"]')
        # print(len(review_by_cat))
        try:
            work_life_balance = review_by_cat[0].text
            compensation_and_benefits = review_by_cat[1].text
            job_security = review_by_cat[2].text
            management = review_by_cat[3].text
            culture = review_by_cat[4].text
        except:
            work_life_balance = ''
            compensation_and_benefits = ''
            job_security = ''
            management = ''
            culture = '' 
    except:
        work_life_balance = ''
        compensation_and_benefits = ''
        job_security = ''
        management = ''
        culture = ''
    
    try:
        # salary = soup.find(class_ = 'css-vqhjqo e37uo190').get_text()
        salary = DRIVER.find_element(By.XPATH, '//div[@class="css-vqhjqo e37uo190"]').text
    except:
        salary = ''
    try:
        # num_jobs = soup.find(class_ = 'css-11v36ww eu4oa1w0').get_text()
        num_jobs = DRIVER.find_element(By.CLASS_NAME, '//div/[@class="css-11v36ww eu4oa1w0"]').text
    except:
        num_jobs = ''
        
    # DRIVER.quit()
    return name, industry, description, founded, link, founder, employees, revenue, rating_2018, rating_2019, rating_2020, rating_2021, rating_2022, work_life_balance, compensation_and_benefits, job_security, management, culture, salary, num_jobs
        

# if __name__ == "main":
data2 = pd.read_csv('out_final2.csv', sep=',', on_bad_lines='skip')
names2 = data2['Company Name']
# print(len(names2))
# data = pd.read_csv('out_final2.csv', sep=',', on_bad_lines='skip')
# names = data['Company Name']
# names3 = []
# for i in names2:
#     names3.append(i)
# for i in names:
#     names3.append(i)
# print(len(names3))
links = get_links(names2)
# print(len(links))
# quit()

filename = 'companies.csv'

if SCRAPED == 0 :
    # write to file
    fields = ['name', 'industry', 'description', 'founded', 'link', 'founder', 'employees', 'revenue', 'rating_2018', 'rating_2019', 'rating_2020', 'rating_2021', 'rating_2022', 'work_life_balance', 'compensation_and_benefits', 'job_security', 'management', 'culture', 'salary', 'num_jobs', 'date']
    with open(filename,'w') as file:
        writer = csv.writer(file)
        writer.writerow(fields)

for i,j in enumerate(links):
    today = date.today()
        
    if i >= START and i < END:
        name, industry, description, founded, link, founder, employees, revenue, rating_2018, rating_2019, rating_2020, rating_2021, rating_2022, work_life_balance, compensation_and_benefits, job_security, management, culture, salary, num_jobs = information(j)
        
        d4 = today.strftime("%b-%d-%Y")
        row = [name, industry, description, founded, link, founder, employees, revenue, rating_2018, rating_2019, rating_2020, rating_2021, rating_2022, work_life_balance, compensation_and_benefits, job_security, management, culture, salary, num_jobs, d4]
        print(i)
        with open(filename,'a') as file:
            writer = csv.writer(file)
            writer.writerow(map(lambda x: [x], row))