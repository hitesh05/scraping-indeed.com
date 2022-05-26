#!/usr/bin/env python3
import enum
from time import sleep
from unicodedata import name
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import csv
from datetime import date

# global variables
NO_OF_PAGES_START = 1
NO_OF_PAGES_END = 100
SCRAPED = 0


def get_link():
    links = [
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Remote&jlid=aaa2b906602aa8f5&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=New%20York%2C%20NY&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Chicago%2C%20IL&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Los%20Angeles%2C%20CA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=San%20Francisco%2C%20CA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Austin%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Houston%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Atlanta%2C%20GA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Washington%2C%20DC&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Boston%2C%20MA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Dallas%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Newport%20News%2C%20VA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Denver%2C%20CO&radius=100&jt=fulltime&explvl=mid_level&sr=directhire',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Seattle%2C%20WA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire'
    ]
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Miami%2C%20FL&radius=100&jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Philadelphia%2C%20PA&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Durham%2C%20NC&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Boulder%2C%20CO&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Pittsburgh%2C%20PA&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Dallas%2C%20TX&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Huston%2C%20PA&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=New%20Jersey&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Detroit%2C%20MI&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Minneapolis%2C%20MN&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%29%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=St.%20Louis%2C%20MO&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%29%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Indianapolis%2C%20IN&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Milwaukee%2C%20WI&radius=100jt=fulltime&explvl=mid_level',
        # 'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Salt%20Lake%20City%2C%20UT&radius=100jt=fulltime&explvl=mid_level'

    # links = [
    #     'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Remote&jlid=aaa2b906602aa8f5&explvl=mid_level&sr=directhire&vjk=83e733840e65ba52'
    # ]
    
    for l in range(len(links)):
        for i in range(NO_OF_PAGES_START, NO_OF_PAGES_END+1):
            page = i
            link = (
                str(links[l])
                + "&start="
                + str(page * 10)
                
            )
            links.append(link)
    return links


def get_links(soup):
    jobs = []
    for job in soup.find_all(
        attrs={
        "class": lambda e: e.startswith("cardOutline tapItem fs-unmask result") if e else False
        },
    ):
        jobs.append(job)
    names = [name.get_text() for name in soup.find_all(
        class_="jcs-JobTitle")]
    location = [loc.get_text() for loc in soup.find_all(
        class_='companyLocation')]

    job_ids = []
    links = []
    easy_apply = []
    urgent_hire = []
    for job in jobs:
        try:
            l = job.find('a', class_='jcs-JobTitle').get('href')
        except:
            l = ''
        x = "https://www.indeed.com" + l
        links.append(x)

        try:
            id = job.find('a', class_='jcs-JobTitle').get('id')
        except:
            id = ''
        job_ids.append(id)
        easy_apply.append(job.find('span', class_='ialbl iaTextBlack') == True)
        urgent_hire.append(job.find(class_='urgentlyHiring') == True)

    print('len of names', len(names))
    print('len of links', len(links))
    return names, job_ids, links, location, easy_apply, urgent_hire


def information(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
    except:
        return '','','','','',False

    try:
        title = soup.find(
            class_='jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating').get_text()
    except:
        title = ''
    try:
        desc = soup.find(
            class_='jobsearch-jobDescriptionText').get_text()
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
    try:
        salary = soup.find(
            'span', class_='icl-u-xs-mr--xs').get_text()
    except:
        salary = ''
    try:
        apply = soup.find(
            'a', class_='icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign').get_text()
        apply_comp = apply.lower() == "apply on company site"        
    except:
        apply_comp = False

    return title, desc, job_posted, company_link, salary, apply_comp


if __name__ == "__main__":
    filename = 'output.csv'
    
    if SCRAPED == 0 :
        # write to file
        fields = ['Job Title','location','Company Name','description','company_link','job_posted','job_ids','easy_apply','urgent hire','salary','remote','crawl_date','apply_comp']
        with open(filename,'w') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    
    today = date.today()

    urls = get_link()
    print('len of urls',len(urls))
    # print(urls)

    names = []
    job_ids = []
    links = []
    location = []
    prev_links = ""
    easy_apply = []
    urgent_hire = []
    x = 0
    for url in range(len(urls)):
        x+=1
        print(x)
        r = requests.get(urls[url])
        soup = BeautifulSoup(r.content, "html5lib")
        n, j, l, loc, easy, urgent = get_links(soup)
        try:
            if l == prev_links:
                prev_links = l
                continue
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
            prev_links = l
        except:
            pass

    # print('here 1')
    remote = ["remote" in i.lower() for i in location]

    titles = []
    descriptions = []
    jobs_posted = []
    company_links = []
    salaries = []
    apply_comps = []

    # print('here 2')
    print(links)

    for i, link in enumerate(links):
        # print('here 3')
        t, d, j, l, s, a = information(link)
        titles.append(t)
        descriptions.append(d)
        jobs_posted.append(j)
        company_links.append(l)
        salaries.append(s)
        apply_comps.append(a)

        d4 = today.strftime("%b-%d-%Y")
        row = [names[i],location[i],t,d,l,j,job_ids[i],easy_apply[i],urgent_hire[i],s,remote[i],d4,a]

        # write to file
        print('here',i)
        with open(filename,'a') as file:
            writer = csv.writer(file)
            writer.writerow(map(lambda x: [x], row))