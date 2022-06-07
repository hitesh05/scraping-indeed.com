#!/usr/bin/env python3

from time import sleep
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import csv
from datetime import date

'''
Requirements:

staffing agency: is there any way to find out? cannot figure out.
Location detail: figure out which companies have this.
Keyword 1,2,3,4: ??
Position count: ??

Indeed firm id: no ID available

UUID: DONE
Easy Apply: on US website. DONE
Urgent hire: DONE
firmname: DONE
Indeed position id: DONE
Job Title: DONE
Salary: DONE
Job description: DONE
Qualifications: DONE
Benefits: DONE
Location: DONE
Job type: To do
Experince level: DONE
Education level: DONE
Industry:DONE
Remote: DONE
Posted time: DONE
Company link: DONE
'''

# global variables
NO_OF_PAGES = 1000
SCRAPED = 0


def get_link(company, location, state):
    
    links = []
    for i in range(NO_OF_PAGES):
        page = i
        link = (
            "https://www.indeed.com/jobs?q="
            + company
            + "&l="
            + location
            + "&start="
            + str(page * 10)
        )
        links.append(link)
    return links


def get_links(soup, company):

    # get list of all jobs
    jobs = soup.find_all(
        "a",
        attrs={
            # for companies in USA
            "class": lambda e: e.startswith("jcs-JobTitle") if e else False
            # for companies in India
            # "class": lambda e: e.startswith("tapItem fs-unmask result") if e else False
        },
    )
    
    # for job in jobs:
    #     print('here')
    names = [name.get_text() for name in soup.find_all(
        class_="turnstileLink companyOverviewLink")]
    location = [loc.get_text() for loc in soup.find_all(
        class_='companyLocation')]

    job_ids = []
    links = []
    to_pop = []
    easy_apply = []
    urgent_hire = []
    for i, job in enumerate(jobs):
        if company.lower() in names[i].lower():  # change
            x = "https://www.indeed.com" + job.get("href")
            links.append(x)
            job_ids.append(job.get("id"))
            easy_apply.append(
                job.find('span', class_='ialbl iaTextBlack') == True)
            urgent_hire.append(job.find(class_='urgentlyHiring') == True)
        else:
            to_pop.append(i)
    else:
        for element in to_pop:
            names.pop(element)
    to_pop.clear()

    return names, job_ids, links, location, easy_apply, urgent_hire


def information(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")

    try:
        title = soup.find(
            class_='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title').get_text()
    except:
        title = ''
    try:
        desc = soup.find(
            class_='jobsearch-JobComponent-description icl-u-xs-mt--md').get_text()
    except:
        desc = ''
    try:
        job_posted = soup.find(
            'span', class_='jobsearch-HiringInsights-entry--text').get_text()
    except:
        job_posted = ''
    try:
        company_link = soup.find(
            class_='icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign').get('href')
    except:
        company_link = ''

    return title, desc, job_posted, company_link


if __name__ == "__main__":

    # original data
    data = pd.read_csv('../organizations_restricted.csv',
                       sep='\t', on_bad_lines='skip')
    # our data
    # data = pd.read_csv('organizations_restricted.csv',
    #                    sep=',', on_bad_lines='skip')

    data['name'] = data['name'].apply(
        lambda x: re.sub('[^A-Za-z0-9\s]+', '', str(x).lower()))

    view1 = data[['name', 'city', 'region']]

    uuid = data['uuid']
    companies = data['name']
    locations = data['city']
    state = ""
    country = data['country_code']

    filename = 'output.csv'
    filename2 = 'progress.csv'
    
    if SCRAPED == 0 :
        # write to file
        fields = ['uuid','company','location','title','description','company_link','job_posted','job_ids','easy_apply','urgent hire']
        with open(filename,'w') as file:
            writer = csv.writer(file)
            writer.writerow(fields)

        fields2 = ['uuid','company','crawl_date','num_jobs','downloaded']
        with open(filename2,'w') as file2:
            writer2 = csv.writer(file2)
            writer2.writerow(fields2)

    for i, (company, location) in enumerate(zip(companies, locations)):

        if i < SCRAPED:
            continue
        
        if pd.isna(company) or pd.isna(location) or country[i] != "USA":
            continue
    
        today = date.today()

        print(f"Scraping for {company} in {location}")

        location = location.replace(" ", "%20")

        urls = get_link(company, location, state)

        names = []
        job_ids = []
        links = []
        location = []
        prev_links = ""
        easy_apply = []
        urgent_hire = []
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html5lib")
            try:
                n, j, l, loc, easy, urgent = get_links(soup, company)
                for i in n:
                    names.append(i)
                for i in j:
                    job_ids.append(i)
                for i in l:
                    links.append(i)
                for i in loc:
                    location.append(i)
                for i in easy:
                    easy_apply.append(i)
                for i in urgent:
                    urgent_hire.append(i)
                if l == prev_links:
                    break
                prev_links = l
            except:
                break


        remote = [i[0:6] == "Remote" for i in location]

        titles = []
        descriptions = []
        jobs_posted = []
        company_links = []

        if len(names) == 0:
            # print('Nothing here\n\n')
            descriptions.append('Nothing Here')
            row = [uuid[i],company,[],[],descriptions,[],[],[],[],[]]

            d4 = today.strftime("%b-%d-%Y")
            row2 = [uuid[i],company,d4,0,True]

            # write to file
            with open(filename,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))

            with open(filename2,'a') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow(map(lambda x: [x], row2))
            continue

        # t,d,j,l = information('https://in.indeed.com/viewjob?jk=5d809fcdeb50fdbe&from=serp&vjs=3')
        for i, link in enumerate(links):

            t, d, j, l = information(link)
            titles.append(t)
            descriptions.append(d)
            jobs_posted.append(j)
            company_links.append(l)

            row = [uuid[i],company,location[i],t,d,l,jobs_posted[i],job_ids[i],easy_apply[i],urgent_hire[i]]

            # write to file
            with open(filename,'a') as file:
                writer = csv.writer(file)
                writer.writerow(map(lambda x: [x], row))

            d4 = today.strftime("%b-%d-%Y")
            row2 = [uuid[i],company,d4,len(names),True]
            with open(filename2,'a') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow(map(lambda x: [x], row2))

            
