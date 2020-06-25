#!/usr/bin/env python
# coding: utf-8

# # Crawling iframe

# In[2]:


from selenium import webdriver


# In[3]:


driver_path = 'webdriver/chromedriver'
driver = webdriver.Chrome(driver_path)


# In[6]:


driver.implicitly_wait(10)


# In[5]:


url = 'http://www.cgv.co.kr/theaters/'

driver.get(url)


# ##### 현재 프레임을 mainframe에 저장

# In[8]:


mainframe = driver.execute_script('return window.frameElement')


# ##### iframe xpath 저장

# In[9]:


iframe = driver.find_element_by_xpath('//*[@id="ifrm_movie_time_table"]')


# ##### frame switch : 현재프레임을 iframe으로 전환

# In[10]:


driver.switch_to_frame(iframe)


# In[11]:


title = driver.find_element_by_xpath('/html/body/div/div[3]/ul/li[1]/div/div[1]/a/strong')
title.text


# ### cgv

# In[1]:


from selenium import webdriver


# In[2]:


driver_path = 'webdriver/chromedriver'
driver = webdriver.Chrome(driver_path)
url = 'http://www.cgv.co.kr/theater'
driver.get(url)


# In[3]:


#드라이버의 현재 프레임을 main_frame안에 저장
main_frame = driver.execute_script("return window.frameElement")


# In[4]:


#iframe xpath 저장
iframe_element = driver.find_element_by_xpath('//*[@id="ifrm_movie_time_table"]')

#프레임 전환 
driver.switch_to_frame(iframe_element)


# In[5]:


movies = driver.find_elements_by_xpath('/html/body/div/div[3]/ul/li')
len(movies), movies


# In[6]:


movie_list = []
for movie in movies:

    grade = movie.find_element_by_class_name('ico-grade').text
    title = movie.find_element_by_xpath('.//div/div[1]/a').text
    timetable = movie.find_elements_by_xpath('.//div/div[2]/div[2]/ul/li')
    
    movie_dict = {
        'title': title,
        'grade': grade,
        'timetable': []
    }
        
    for table in  timetable:
        time_t = table.find_element_by_xpath('.//em').text
        seat_t = table.find_element_by_xpath('.//span').text
        movie_dict['timetable'].append(
            {
                'time': time_t,
                'seat': seat_t
            }
        )
    movie_list.append(movie_dict)
    


# In[7]:


import pprint

pprint.pprint(movie_list)


# - 다른 지점의 영화 정보를 가져오고 싶다면?

# In[8]:


# 다시 프레임 전환 ; iframe -> mainframe
driver.switch_to_frame(main_frame)


# In[ ]:




