from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time

#creating a service object to share our chromedriver path
s= Service(r'C:\Users\Shivam SDE\OneDrive\Desktop\chromedriver.exe')

webdriver.Chrome(service=s)
#lets save driver object into a variable

driver=webdriver.Chrome(service=s)

driver.get('https://www.ajio.com/s/deodrants-5260-44722')

old_height = driver.execute_script('return document.body.scrollHeight')

counter = 1
while True:


    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)

    new_height = driver.execute_script('return document.body.scrollHeight')

    print(counter)
    counter += 1
    print(old_height)
    print(new_height)

    if new_height == old_height:
        break

    old_height = new_height



html = driver.page_source

with open('ajio.html','w',encoding='utf-8') as f:
    f.write(html)