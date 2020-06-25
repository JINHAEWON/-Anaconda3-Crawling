#!/usr/bin/env python
# coding: utf-8

# In[19]:


#1번 
#원하는 웹툰찾기 
#원하는 웹툰 = > "신의탑"
#findurl => 이동할 url 적혀있음 
find_title = "신의 탑"


import requests
base_url = 'https://comic.naver.com'
url = base_url + '/webtoon/weekdayList.nhn?week=mon'
resp = requests.get(url)

from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.content,'lxml')

li_tag = soup.select('ul.img_list li') #(list로 저장됨 )
for li in li_tag:
    title = li.select('dl dt a')[0]['title']
    if title == find_title:
        find_url = li.select('dl dt a')[0]['href']
        break

# print(find_url)
        
#2번
#원하는 웹툰 사이트로 이동 
resp = requests.get(base_url + find_url)
soup = BeautifulSoup(resp.content,'lxml')

#3번 
#title 갖고오기
td_tag = soup.select('table.viewList tr td.title')


#4번 화면 전환하기 
page_query ={}
for page in range(43):
    for td in td_tag:
        title = td.text.strip() #strip 양옆에있는것을 빼는 코드 
        title_list.append(title)
    #4번    
    page_query['page']=page+1
    resp=requests.get(base_url+find_url,page_query)
    soup=BeautifulSoup(resp.content,'lxml')
    td_tag = soup.select('table.viewList tr td.title')
    print('{} page finished..'.format(page)) # 중간에 코드를 찍어보면서 돌아가는지확인
    
#출력 
import pprint
pprint.pprint(title_list)


# In[ ]:




