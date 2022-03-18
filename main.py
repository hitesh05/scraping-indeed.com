import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup

'''
Requirements:
UUID: to be carried over
Easy Apply: on US website. check how to do it
Urgent hire: not on Indian website
staffing agency: is there any way to find out?
Location detail: figure out which companies have this
Keyword 1,2,3,4: ??
Position count: ??

Indeed firm id: no ID available

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


def get_link(company, location, state):
    links = []
    for i in range(1):
        page = i
        link = (
            "https://in.indeed.com/jobs?q="
            + company
            + "&l="
            + location
            + "&start="
            + str(page * 10)
        )
        links.append(link)
    return links


def get_links(soup, company):
    links = []
    jobs = soup.find_all(
        "a",
        attrs={
            "class": lambda e: e.startswith("tapItem fs-unmask result") if e else False
        },
    )  # got list of all jobs
    names = soup.find_all(class_="turnstileLink companyOverviewLink")
    location = soup.find_all(class_='companyLocation')
    iter = 0
    for i in names:
        names[iter] = i.get_text()
        location[iter] = location[iter].get_text()
        iter += 1

    iter = 0
    job_ids = []
    for i in jobs:
        if names[iter] == company:
            x = "https://in.indeed.com" + i.get("href")
            links.append(x)
            job_ids.append(i.get("id"))
        else:
            names.pop(iter)
        iter += 1
    return names, job_ids, links, location

def information(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    title = soup.find(class_='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title').get_text()
    desc = soup.find(class_='jobsearch-JobComponent-description icl-u-xs-mt--md').get_text()
    job_posted = soup.find('span', class_='jobsearch-HiringInsights-entry--text').get_text()
    company_link = soup.find(class_='icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign')
    company_link = company_link.get('href')
    return title,desc,job_posted, company_link
    

if __name__ == "__main__":
    company = "Microsoft"
    location = "Hyderabad"
    state = ""
    urls = get_link(company, location, state)

    names = []
    job_ids = []
    links = []
    location = []
    prev_links = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        n, j, l, loc = get_links(soup, company)
        for i in n:
            names.append(i)
        for i in j:
            job_ids.append(i)
        for i in l:
            links.append(i)
        for i in loc:
            location.append(i)
        if l == prev_links:
            break
        prev_links = l
    remote = [i[0:6] == "Remote" for i in location]
    titles = []
    descriptions = []
    jobs_posted = []
    company_links = []
    
    # t,d,j,l = information('https://in.indeed.com/viewjob?jk=5d809fcdeb50fdbe&from=serp&vjs=3')
    for i in links:
        t,d,j, l = information(i)
        titles.append(t)
        descriptions.append(d)
        jobs_posted.append(j)
        company_links.append(l)