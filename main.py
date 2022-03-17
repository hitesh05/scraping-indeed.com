import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup

def get_link(company, location):
    link = "https://in.indeed.com/jobs?q=" + company + "&l=" + location
    return link


def get_links(soup):
    """
    handle number of pages
    """

    links = []
    jobs = soup.find_all(
        "a",
        attrs={
            "class": lambda e: e.startswith("tapItem fs-unmask result") if e else False
        },
    )  # got list of all jobs
    names = soup.find_all(class_='turnstileLink companyOverviewLink')
    iter = 0
    for i in names:
        names[iter] = i.get_text()
        iter+=1
     
    job_ids = []    
    for i in jobs:
        x = 'https://in.indeed.com'+i.get('href')
        links.append(x)
        job_ids.append(i.get('id'))
    return names,job_ids,links


company = "Microsoft"
location = "hyderabad"
url = get_link(company, location)

r = requests.get(url)
soup = BeautifulSoup(r.content, "html5lib")

names,job_ids,links = get_links(soup)
print(names,job_ids,links)

