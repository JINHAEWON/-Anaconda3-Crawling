#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


# In[6]:


result = requests.get('https://comic.naver.com/webtoon/weekday.nhn')

soup = BeautifulSoup(result.content, 'lxml')
soup


# In[7]:


week_cols = soup.select('div.col div.col_inner')

webtoon_dict = {}
for col in week_cols:
    weekday = col.find('span')
#     print(weekday.text)
    webtoons = col.select('ul li a')

    for webtoon in webtoons:
        title = webtoon.text
        link = webtoon['href']
        titleId = re.findall('[0-9]+',link)
#         print(titleId)
        if not '\n' in title:
            webtoon_dict[title]  = {
                'title': title,
                'link': link,
                'title_id': titleId[0]
            }
pprint(webtoon_dict)


# - href 는 a 태그의 하이퍼링크 url이 들어가 있다.
# - 그런데!! href 값을 보니 /부터 시작한다?
# - /~~ = 리소스경로!! (+ ?~~ = 쿼리스트링)
# 
# **결론**
# - '프로토콜://주소값/' 가져와서 이거 뒤에 href값(리소스경로+쿼리스트링) 붙이자.
# - 어떤 프로토콜://주소값을 긁어와야되는지는 어떻게 알지? = href 클릭해보면 안다.

# In[14]:


url_webtoon = 'http://comic.naver.com'

for idx, toon in enumerate(webtoon_dict):
    result = requests.get(url_webtoon + webtoon_dict[toon]['link'])
    soup = BeautifulSoup(result.content)
    
    current_href = soup.select('table.viewList tr td.title a')[0]['href']
    current_no = re.findall('no=([0-9]+)', current_href)[0] #몇화까지 나왔는지 확인하는것 
#     print(current_no)

    #'신의탑' : {'title': , 'link': , 'titleId': } 에다가 'current_no'도 추가    
    webtoon_dict[toon]['current_no'] = current_no
    
    #진행 상황 체크 (출력)
    print('{} 완료.. {}/{}'.format(toon, idx, len(webtoon_dict)))    
    if (idx+1)%40 == 0:
        print('{} 완료.. {}/{}'.format(toon, idx+1, len(webtoon_dict)))


# In[13]:


pprint(webtoon_dict)


# In[ ]:





# - requests.get(url, params)를 했을 때 result.content에 "실패"라고 뜬다면  
# 
# 1) network에 들어가서 요청헤더(requests header)를 확인하자.  
# 2) 명시되어있는 애들을 복사해서 headers에 dictionary형태로 넣자.  
# 3) requests.get(url, params, headers) 추가해서 요청하자.

# In[79]:


title = input('웹툰명:')
titleId = webtoon_dict[title]['title_id']
current_no = webtoon_dict[title]['current_no'] # 현재까지 몇화까지 나왔는지 checking 해주는 것
page_no = 1 


# In[80]:


comment_url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json'

params = {
    'ticket':'comic',
    'templateId':'webtoon',
    'pool':'cbox3',
    '_callback':'jQuery112406460093114128636_1560319830291',
    'lang':'ko',
    'country':'KR',
    'objectId':'{}_{}'.format(titleId, current_no), # titleId_current_no // titleid -> 모든 웹툰의 댓글을 갖고오기위해 변수화함
    'pageSize':15,
    'indexSize':10,
    'listType':'OBJECT',
    'pageType':'default',
    'page':page_no,
    'refresh':'true',
    'sort':'best',
    '_':1560319830294
}

headers = {
    'Referer': 'https://comic.naver.com/comment/comment.nhn?titleId={}&no={}'.format(titleId,current_no)
} # network tap 에서 request header에서 user-Agents 이외의 어떤 값이 있다면 그걸 똑같이 불러와줘야함 

result = requests.get(comment_url, headers=headers, params=params)
result


# In[81]:


result.content


# In[82]:


result_update = re.findall('jQuery[0-9_(]+(.+?)\);',result.text)[0]
result_update


# In[83]:


import json


# In[84]:


#result.content(JSON) -> dictionary로 변환
result_json = json.loads(result_update)
result_json #'result'->'commentList'->['contents']


# In[85]:


result_json['result']


# In[86]:


result_json['result']['commentList']


# In[87]:


len(result_json['result']['commentList'])


# In[88]:


commentList = result_json['result']['commentList']
for i, comment in enumerate(commentList): #comment = dictionary
    print(i+1, comment['contents'])


# In[ ]:




