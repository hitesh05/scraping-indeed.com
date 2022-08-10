import enum
from itertools import count
import pandas as pd
import csv
import re

# editing output.csv file

# filename = 'out_final2.csv'
# data = pd.read_csv('output.csv',sep=',',on_bad_lines='skip')
    
# fields = ['Job Title','location','Company Name','description','company_link','job_posted','job_ids','easy_apply','urgent hire','salary','remote','crawl_date','apply_comp']
# with open(filename,'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(fields)
# s = set()
# for i in data.values:
#     row = []
#     for j in range(len(i)):
#         # i[j] = i[j][2:-2]
#         if j == 2 and str(i[j][-9:-2]).lower() == "reviews":
#             i[j] = i[j][:-10]
#             i[j] += "']"
#         row.append(i[j])
#     if str(row) not in s:
#         with open(filename,'a') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(map(lambda x: x, row))
#     s.add(str(row))
            
# df = pd.read_csv('out_final2.csv')

# for i,j in enumerate(df['Company Name']):
#     j = re.sub('.com','',j)
#     j = re.sub('[0-9]','',j)
#     j = re.sub(',','',j)
#     df.loc[i,'Company Name'] = j
# df.drop('easy_apply', inplace=True, axis=1)
# df.drop('urgent hire', inplace=True, axis=1)
# df.to_csv('out_final2.csv', index = False)


# replacing faulty entries from companies.csv:

df = pd.read_csv('companies.csv')
df2 = pd.DataFrame()

# for i,j in enumerate(df['num_jobs']):
#     if j == "['']":
#         df.loc[i, 'num_jobs'] = ['']
#     else:
#         b = 0
#         for x,y in enumerate(j):
#             if y == '}':
#                 b = x
#         b+=1
#         df.loc[i, 'num_jobs'] = [j[b:-2]]

x = 0 
y=0
for i,j in enumerate(df['name']):
    if j == "['']":
        df.drop(df.index[x], inplace=True)
    else:
        x+=1
    
#     j = re.sub('\s','-',j)
#     j = re.sub('.com','',j)
#     j = re.sub('[0-9]','',j)
#     j = re.sub(',','',j)
#     df.loc[i,'name'] = [j]
        
# for i,j in enumerate(df['salary']):
#     j = str(j)
#     if j == "['']":
#         df.loc[i, 'salary'] = ['']
#     else:
#         b = 0
#         for x,y in enumerate(j):
#             if y == '}':
#                 b = x
#         b+=1
#         df.loc[i, 'salary'] = [j[b:-2]]

# for i,j in enumerate(df['industry']):
#     a = ['1','2','3','4','5','6','7','8','9','0','$']
#     for x in a:
#         if x in str(j):
#             df.loc[i,'industry'] = ['']
#             break
      
df.to_csv('companies.csv', index=False)