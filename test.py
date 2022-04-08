from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from pprint import pprint

from urllib.parse import urljoin
import webbrowser
import sys
import json
s = requests.Session()

# initialize an HTTP session
session = HTMLSession()

headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")

x = get_all_forms('http://www.indeed.com')
# print(x)


url = 'http://www.indeed.com'

d = {}
d['q'] = 'Google'
d['l'] = 'Seattle'
response = s.get(url,headers=headers, params=d)
print(response.text)
content = response.content
soup = BeautifulSoup(content,"lxml")

# print(soup) # is always an empty list