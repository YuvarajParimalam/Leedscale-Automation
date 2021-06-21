import requests
from bs4 import BeautifulSoup as soup
import json
import pandas as pd
import configparser
import os
import time
from urllib.parse import quote
from cleanco import cleanco

config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
proxy = config.get('Proxy', 'Proxy')
proxies = {"http":'http://'+proxy, "https":'http://'+proxy}

ua={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def Company_Cleaner(company):
    company=company.replace('Holding','')
    company=cleanco(company).clean_name()
    return company

def Search_Contact(row,domain):
    if domain=='Linkedin':
        companydetail=row['First Name']+" "+row['Last Name']+" "+row['Job Title']+" "+row['Company Name']+' '+str(domain)
        companydetail=quote(companydetail, safe='')
    else:
        companydetail=Company_Cleaner(row['Company Name'])+' '+str(domain)
        companydetail=quote(companydetail, safe='')
    url='https://www.google.com/search?q={}'.format(companydetail)
    print(url)
    for _ in range(5):
        a=requests.get(url,headers=ua)
        if a.status_code==200:
            break
    time.sleep(2)
    r=soup(a.text,'html.parser')
    atag=r.findAll('div',class_='yuRUbf')[0]
    link=atag.find('a')['href']
    print(link)
    return link

        