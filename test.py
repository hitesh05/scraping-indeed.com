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
# for i in data.values:
#     row = []
#     for j in range(len(i)):
#         # i[j] = i[j][2:-2]
#         if j == 2 and str(i[j][-9:-2]).lower() == "reviews":
#             i[j] = i[j][:-10]
#             i[j] += "']"
#         row.append(i[j])
#     with open(filename,'a') as file:
#             writer = csv.writer(file)
#             writer.writerow(map(lambda x: x, row))
            
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

# df = pd.read_csv('companies.csv')
# df2 = pd.DataFrame()

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

# x = 0 
# for i,j in enumerate(df['name']):
#     j = j[2:-2]
#     if j == '':
#         df.drop(df.index[x], inplace=True)
#     else:
#         x+=1
    
    # j = re.sub('\s','-',j)
    # j = re.sub('.com','',j)
    # j = re.sub('[0-9]','',j)
    # j = re.sub(',','',j)
    # df.loc[i,'name'] = [j]
        
# for i,j in enumerate(df['salary']):
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
#         if x in j:
#             df.loc[i,'industry'] = ['']
#             break
      

# a = ['Unnamed: 21']
# for i in range(22,50):
#     s = a[0][:-2]
#     s += str(i)
#     a.append(s)

# for i in range(len(a)):
#     df.drop(a[i], inplace=True, axis=1)  
# df.to_csv('companies.csv', index=False)


# making changes to out_final:

# df = pd.read_csv('out_final.csv')

# for i,j in enumerate(df['Company Name']):
#     j = re.sub('.com','',j)
#     j = re.sub('[0-9]','',j)
#     j = re.sub(',','',j)
#     df.loc[i,'Company Name'] = j

# df.drop('easy_apply', inplace=True, axis=1)
# df.drop('urgent hire', inplace=True, axis=1)
    
# df.to_csv('out_final2.csv', index = False)

# filename1 = 'reviews1.csv'
# filename2 = 'reviews2.csv'
# filename3 = 'reviews3.csv'
# filename4 = 'reviews4.csv'

# x = "review_"
# row1 = []
# row1.append("Company Name")
# row2 = []
# row2.append("Company Name")
# row3 = []   
# row3.append("Company Name")
# row4 = []
# row4.append("Company Name")

# for i in range(1,101):
#     y = x + str(i)
#     row1.append(y)
    
# with open(filename1,'a') as file:
#     writer = csv.writer(file)
#     writer.writerow(map(lambda x: x, row1))
    
# for i in range(1,501):
#     y = x + str(i)
#     row2.append(y)
    
# with open(filename2,'a') as file:
#     writer = csv.writer(file)
#     writer.writerow(map(lambda x: [x], row2))
    
# for i in range(1,1001):
#     y = x + str(i)
#     row3.append(y)
    
# with open(filename3,'a') as file:
#     writer = csv.writer(file)
#     writer.writerow(map(lambda x: [x], row3))
    
# for i in range(1,2001):
#     y = x + str(i)
#     row4.append(y)
    
# with open(filename4,'a') as file:
#     writer = csv.writer(file)
#     writer.writerow(map(lambda x: [x], row4))

# df1 = pd.read_csv('reviews1.csv')
# names1 = list(df1['Company Name'])

# df2 = pd.read_csv('companies.csv')
# names2 = list(df2['name'])

# for i,j in enumerate(names1):
#     j = j[2:-2]
#     j = j.lower()
#     j = re.sub('-', ' ', j)
#     names1[i] = j
    
# for i,j in enumerate(names2):
#     j = j[2:-2]
#     j = j.lower()
#     j = re.sub('-', ' ', j)
#     names2[i] = j
# print(len(names2))
    
# for i in names1:
#     if i not in names2:
#         names2.append(i)
        
# print(len(names2))