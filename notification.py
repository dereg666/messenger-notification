# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import sys
from selenium.webdriver.common.action_chains import ActionChains

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

driver = webdriver.Chrome()

def fb_login():
    driver.get("http://www.facebook.org")
    assert "Facebook" in driver.title
    elem = driver.find_element_by_id("email")
    elem.send_keys('')        #輸入FB帳號
    elem = driver.find_element_by_id("pass")
    elem.send_keys('')      #輸入FB密碼
    elem.send_keys(Keys.RETURN)
    time.sleep(5)

def notification():
    try:
        elem = driver.find_element_by_css_selector("#fbNotificationsJewel")
        elem.click()
        time.sleep(3)
        
        elem = driver.find_element_by_class_name('fwb')
        elem.click()
        time.sleep(5)
        get_link()
    except:
        driver.get("https://www.facebook.com/")
        time.sleep(5)
        notification()

def get_link():
    global web
    soup=BeautifulSoup(driver.page_source,'html.parser')
    url=[]
    links=soup.find_all('span',class_='fsm fwn fcg')
    #s=soup.find_all('a',href=True)
    for link in links:
        url.append(link.a.get("href"))
        #print(link.a.get("href"))
    #print(url[1])
    if web==url[1]:
        time.sleep(5)
        notification()
    else:
        web=url[1]
        driver.get("http://www.facebook.com"+url[1])
        time.sleep(5)
        check_keyword()

def check_keyword(ref):
    #driver.get('https://www.facebook.com/groups/closeout/permalink/1305811419527251/')
    soup=BeautifulSoup(driver.page_source,'html.parser')
    paragraphs=soup.find_all('p')
    try:s=soup.find('span',class_='_5s8v').next_element.text.strip()
    except:s=''
    #print(s)
    for p in paragraphs:
            s+=p.text.strip()
    if len(s)<150:
        for k in Keyword:
            if k in s:
                try:
                    print(k)
                    print(s.translate(non_bmp_map))
                    #print(len(s))
                except:pass
                send_msg(k,s,ref)
                break

def send_msg2(k,s,ref):
    #driver.get("https://www.facebook.com/messages/t/100006010900890")
    driver.get("https://www.facebook.com/messages/t/1530805176993941")
    try:
        elem = driver.find_element_by_class_name('_4rv9')
        for i in range(3):
            elem.click()
            time.sleep(10)
    except:send_msg(k,s,ref)

def send_msg(k,s,ref):
    #driver.get("https://www.facebook.com/messages/t/100006010900890")
    driver.get("https://www.facebook.com/messages/t/1530805176993941")
    elem = ActionChains(driver)
    #time.sleep(10)
    #print('aa')
    #elem.send_keys('測試中')
    #elem.send_keys(Keys.RETURN) 
    try:
    #elem = driver.find_element_by_class_name('_1mf')
        elem.send_keys('關鍵字[%s]有新貼文\n'%k)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(s.translate(non_bmp_map))
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(ref)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        for i in range(3):
            elem.perform()
            time.sleep(10)
    except:
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
        elem.perform()
        send_msg2(k,s,ref)

def group_monitor(gourp):
    driver.get(gourp)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    span=soup.find_all('span',class_='fsm fwn fcg')
    for t in span:
        #print(t.text)
        if ('分鐘' in t.text and int(''.join(filter(str.isdigit,t.text)))==1) or '剛剛' in t.text:
            ref="http://www.facebook.com"+t.a.get("href")
            driver.get(ref)
            check_keyword(ref)

def loop():
    try:
        group_monitor("https://www.facebook.com/groups/closeout/")
        group_monitor("https://www.facebook.com/groups/NTU.Head/")
        group_monitor("https://www.facebook.com/groups/NTU.Forsale/")
        group_monitor("https://www.facebook.com/groups/414259302086849/")
        #group_monitor("https://www.facebook.com/groups/709018975957629/")
    except:
        loop()

fb_login()

#send_msg()

Keyword=['漢堡','豆漿','披薩','izza','餐盒','便當','早餐','午餐','晚餐','食物','會議','研討會','營隊','自備','容器','葷','點心','茶點','外燴','飲料','免費','咖哩','肉','飯','麵','紅茶','綠茶','奶茶'] #刪除關鍵字['自取','剩','素',,'活動']
web=''

while 1:
    loop()
    
    

    

    
