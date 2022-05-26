from itertools import count
import pandas as pd

# data = pd.read_csv('../organizations_restricted.csv',
#                        sep='\t', on_bad_lines='skip')

# companies = data['name']
# locations = data['city']
# country = data['country_code']
# print(country.value_counts().to_string())

# x = 0
# for i, (company, location) in enumerate(zip(companies, locations)):
#     if country[i] == "CAN":
#         x += 1
        
# print(x)

# check.py:

# df = pd.read_csv('progress.csv',sep=',')
# jobs = df['num_jobs']
# names = df['company']
# x = 0
# y = 0

# hits = set()

# for i in jobs:
#     y += 1
#     job = int(i[1])
#     if job > 0:
#         x += 1
#         hits.add(names[y-1])
        
# print(x)
# print(hits)

# df = pd.read_csv('output.csv',sep=',')
# desc = df['description']
# x = 0

# for i in desc:
#     x+=1
#     if i[3:-3]!="Nothing Here":
#         print(df.iloc[x])
#         break
# print(desc[1][3:-3]=="Nothing Here")

# https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&l=New%20York&radius=100&explvl=mid_level&sr=directhire&start=10000&vjk=c7cf8a8af979a5a1

'''
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Remote&jlid=aaa2b906602aa8f5&explvl=mid_level&sr=directhire&vjk=6295bc9b38a2ef0d
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=New%20York%2C%20NY&radius=100&jt=fulltime&explvl=mid_level&start=1000
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Chicago%2C%20IL&jlid=402d6ad50e16c894&explvl=mid_level&sr=directhire&vjk=793a53a518c026b9
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Los%20Angeles%2C%20CA&jlid=d05a4fe50c5af0a8&explvl=mid_level&sr=directhire&vjk=28afa64fdfcbee30
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=San%20Francisco%2C%20CA&jlid=6cf5e6d389fd6d6b&explvl=mid_level&sr=directhire&vjk=006f204d6f954146
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Austin%2C%20TX&jlid=d2a39b6d57d82344&explvl=mid_level&sr=directhire&vjk=3a4e50cfa86001ed
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Houston%2C%20TX&jlid=fcd454bec6232f93&explvl=mid_level&sr=directhire&vjk=f05f90d09424a1d2
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Atlanta%2C%20GA&jlid=966e6327a98f7e81&explvl=mid_level&sr=directhire&vjk=a801c770874acaa0
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Washington%2C%20DC&jlid=c08ec92d8c031faa&explvl=mid_level&sr=directhire&vjk=0d90b58a18493590
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Boston%2C%20MA&jlid=e167aeb8a259bcac&explvl=mid_level&sr=directhire&vjk=a3fd742174ca4480
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Dallas%2C%20TX&jlid=c9b29a6e6a9f190c&explvl=mid_level&sr=directhire&vjk=c4d700d2f35070b8
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Newport%20News%2C%20VA&jlid=a8cc372befad335e&explvl=mid_level&sr=directhire&vjk=35a28efe70c54d7a
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Denver%2C%20CO&jlid=3ff9c6509d39a5e5&explvl=mid_level&sr=directhire&vjk=0e821b03f26d77ef
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&rbl=Seattle%2C%20WA&jlid=1e8a7dce52945215&explvl=mid_level&sr=directhire&vjk=e9a20f34bae78184
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Miami%2C%20FL&radius=100&jt=fulltime&explvl=mid_level&vjk=b92bc83421297329
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Philadelphia%2C%20PA&radius=100jt=fulltime&explvl=mid_level&vjk=0a923e3fb4074f9c
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Durham%2C%20NC&radius=100jt=fulltime&explvl=mid_level&start=1000
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=Boulder%2C%20CO&radius=100jt=fulltime&explvl=mid_level&vjk=ed71218f9ef421b2
https://www.indeed.com/jobs?q=(executive%20or%20manager%20or%20product%20or%20market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-IT%20%2450%2C000%2B&explvl=mid_level&sr=directhire&start=10&vjk=a801c770874acaa0
https://www.indeed.com/jobs?q=(executive%20or%20Manager%20or%20Product%20or%20Market)%20-assistant%20-associate%20-junior%20-analyst%20-architect%20-engineer%20-scientist%20-representative%20-researcher%20-teacher%20-accounting%20-it%20%2450%2C000%2B&l=New%20York%2C%20NY&radius=100&jt=fulltime&explvl=mid_level&fromage=7&start=1000

'''

for i in range(5):
    if i == 1:
        continue
    print(i)
