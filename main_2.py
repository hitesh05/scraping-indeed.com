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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

S=Service(ChromeDriverManager().install())
DRIVER = webdriver.Chrome(service=S)

# global variables
NO_OF_PAGES_START = 1
NO_OF_PAGES_END = 45
SCRAPED = 0


def get_link():
    links = [
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Remote&jlid=aaa2b906602aa8f5&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=New%20York%2C%20NY&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Chicago%2C%20IL&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Los%20Angeles%2C%20CA&radius=100&jt=fuldirecthireltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=San%20Francisco%2C%20CA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Austin%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Houston%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Atlanta%2C%20GA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Washington%2C%20DC&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Boston%2C%20MA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Dallas%2C%20TX&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Newport%20News%2C%20VA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Denver%2C%20CO&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Seattle%2C%20WA&radius=100&jt=fulltime&explvl=mid_level&sr=directhire&fromage=3'
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Miami%2C%20FL&radius=100&jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Philadelphia%2C%20PA&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Durham%2C%20NC&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Boulder%2C%20CO&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Pittsburgh%2C%20PA&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Dallas%2C%20TX&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Huston%2C%20PA&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=New%20Jersey&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Detroit%2C%20MI&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Minneapolis%2C%20MN&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=St.%20Louis%2C%20MO&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Indianapolis%2C%20IN&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Milwaukee%2C%20WI&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Salt%20Lake%20City%2C%20UT&radius=100jt=fulltime&explvl=mid_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Remote&jlid=aaa2b906602aa8f5&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=New%20York%2C%20NY&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Chicago%2C%20IL&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Los%20Angeles%2C%20CA&radius=100&jt=fuldirecthireltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=San%20Francisco%2C%20CA&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Austin%2C%20TX&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Houston%2C%20TX&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Atlanta%2C%20GA&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Washington%2C%20DC&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Boston%2C%20MA&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Dallas%2C%20TX&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Newport%20News%2C%20VA&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Denver%2C%20CO&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Seattle%2C%20WA&radius=100&jt=fulltime&explvl=senior_level&sr=directhire&fromage=3'
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Miami%2C%20FL&radius=100&jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Philadelphia%2C%20PA&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Durham%2C%20NC&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Boulder%2C%20CO&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Pittsburgh%2C%20PA&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Dallas%2C%20TX&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Huston%2C%20PA&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=New%20Jersey&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Detroit%2C%20MI&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Minneapolis%2C%20MN&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=St.%20Louis%2C%20MO&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=%28executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Indianapolis%2C%20IN&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Milwaukee%2C%20WI&radius=100jt=fulltime&explvl=senior_level&fromage=3',
        'https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market%20or%20president%20or%20vp%20or%20vice-president%20or%20officer%20or%20Operation%20or%20development%20or%20growth%20or%20finan%20or%20advertis%20or%20client%20or%20technol)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-budget%20%2450%2C000%2B&l=Salt%20Lake%20City%2C%20UT&radius=100jt=fulltime&explvl=senior_level&fromage=3'
    ]

    for l in range(0,56):
        for i in range(NO_OF_PAGES_START, NO_OF_PAGES_END+1):
            page = i
            link = (
                str(links[l])
                + "&start="
                + str(page * 10)
                
            )
            links.append(link)
    return links


def get_links(url):
    try:
        DRIVER.get(url)
    except:
        return [],[],[],[]
    jobs = []
    # for job in soup.find_all(
    #     attrs={
    #     "class": lambda e: e.startswith("cardOutline tapItem fs-unmask result") if e else False
    #     },
    # ):
    #     jobs.append(job)
        
    for job in DRIVER.find_elements(By.XPATH, '//div[starts-with(@class,"cardOutline tapItem fs-unmask result")]'):
        jobs.append(job)

    names = [name.text for name in DRIVER.find_elements(By.CLASS_NAME, "jcs-JobTitle")]

    location = [loc.text for loc in DRIVER.find_elements(By.CLASS_NAME, 'companyLocation')]

    job_ids = []
    links = []
    # salaries = []
    
    for link in DRIVER.find_elements(By.XPATH, '//a[starts-with(@class,"jcs-JobTitle")]'):
        try:
            l = link.get_attribute('href')
        except:
            l = ''
        links.append(l)
        
    for ids in DRIVER.find_elements(By.XPATH, '//a[starts-with(@class,"jcs-JobTitle")]'):
        try:
            id = ids.get_attribute('id')
        except:
            id = ''
        job_ids.append(id)
        
    # try:
    #     s = DRIVER.find_elements(By.CLASS_NAME,"resultContent")
    #     for i in s:
    #         salaries.append(i.text)
    # except:
    #     salaries = []
          
    return names, job_ids, links, location


def information(url):
    try:
        # r = requests.get(url)
        # soup = BeautifulSoup(r.content, "html5lib") 
        DRIVER.get(url)
    except:
        return '','','','','',False, ''

    try:
        title = DRIVER.find_element(By.XPATH, '//div[@class="jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating"]').text
        # title = soup.find(
        #     class_='jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating').get_text()
    except:
        title = ''
    try:
        desc = DRIVER.find_element(By.CLASS_NAME, 'jobsearch-jobDescriptionText').text
        # desc = soup.find(
        #     class_='jobsearch-jobDescriptionText').get_text()
    except:
        desc = ''
    try:
        job_posted = DRIVER.find_element(By.XPATH, '//span[@class="jobsearch-HiringInsights-entry--text"]').text
        # job_posted = soup.find(
        #     'span', class_='jobsearch-HiringInsights-entry--text').get_text()
    except:
        job_posted = ''
    try:
        company_link = DRIVER.find_element(By.CLASS_NAME, 'icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign').get_attribute('href')
        # company_link = soup.find(
        #     class_='icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign').get('href')
    except:
        company_link = ''
    try:
        salary = DRIVER.find_element(By.XPATH, '//span[@class="icl-u-xs-mr--xs"]').text
        # salary = soup.find(
        #     'span', class_='icl-u-xs-mr--xs').get_text()
    except:
        salary = ''
    try:
        apply = DRIVER.find_element(By.XPATH, '//a[@class="icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign"]')
        # apply = soup.find(
        #     'a', class_='icl-Button icl-Button--primary icl-Button--md icl-Button--block jobsearch-CallToApply-applyButton-newDesign').get_text()
        apply_comp = apply.lower() == "apply on company site"        
    except:
        apply_comp = False
    
    try:
        salary3 = DRIVER.find_element(By.CLASS_NAME, "css-1lyr5hv eu4oa1w0").text
    except:
        salary3 = ''
        
    # print(title,desc,job_posted,company_link,salary,apply_comp)
    # DRIVER.quit()
    # quit()

    return title, desc, job_posted, company_link, salary, apply_comp, salary3


if __name__ == "__main__":
    filename = 'output.csv'
    
    if SCRAPED == 0 :
        # write to file
        fields = ['Job Title','location','Company Name','description','company_link','job_posted','job_ids','salary','remote','crawl_date','apply_comp', 'salary3']
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
    salary3 = []
    # easy_apply = []
    # urgent_hire = []
    x = 0
    for url in range(len(urls)):
    # for url in range(1):
        x+=1
        # try:
        #     r = requests.get(urls[url])
        #     soup = BeautifulSoup(r.content, "html5lib")
        # except:
        #     continue
        n, j, l, loc= get_links(urls[url])
        print(x)
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
            # for i in s:
            #     salary3.append(i)
            prev_links = l
        except:
            pass

    remote = ["remote" in i.lower() for i in location]

    titles = []
    descriptions = []
    jobs_posted = []
    company_links = []
    salaries = []
    apply_comps = []
    salary3 = []

    for i, link in enumerate(links):
        # print('here 3')
        t, d, j, l, s, a, s3 = information(link)
        titles.append(t)
        descriptions.append(d)
        jobs_posted.append(j)
        company_links.append(l)
        salaries.append(s)
        apply_comps.append(a)
        salary3.append(s3)

        d4 = today.strftime("%b-%d-%Y")
        row = [names[i],location[i],t,d,l,j,job_ids[i],s,remote[i],d4,a,salary3[i]]

        # write to file
        print('here',i)
        with open(filename,'a') as file:
            writer = csv.writer(file)
            writer.writerow(map(lambda x: [x], row))