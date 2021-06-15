import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import time
import sys
import json
import configparser
import os

config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
proxy = config.get('Proxy', 'Proxy')
proxies = {"http": proxy, "https": proxy}
UserName=config.get('LinkedIn','UserName')
PassWord=config.get('LinkedIn','PassWord')

# login to Linkedin to get the Session details
def Login():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    uname=driver.find_element_by_name('session_key')
    uname.send_keys(UserName)
    passwd=driver.find_element_by_name('session_password')
    passwd.send_keys(PassWord)
    driver.find_element_by_xpath('//button[@class="btn__primary--large from__button--floating"]').click()
    time.sleep(10)
    df=pd.DataFrame(driver.get_cookies())
    filePath=os.path.join(os.getcwd(),'cookie')
    df.to_csv(filePath+'/session.csv')
    driver.quit()
    return df

def get_Headers(df):
    li_at=df.loc[df['name'] == 'li_at', 'value'].item()
    jsession=df.loc[df['name'] == 'JSESSIONID', 'value'].item()
    cookie='JSESSIONID='+str(jsession)+'; li_at='+str(li_at)+';'
    headers = {
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': str(jsession).replace('"',''),
    'cookie': str(cookie)
    }
    return headers

def Extract_Contact(source,url):
    jsonContent=json.loads(source)
    nameBlock=pd.DataFrame(jsonContent['included'])
    nameBlock=nameBlock[nameBlock['$type']=='com.linkedin.voyager.dash.identity.profile.Profile']
    df=pd.DataFrame(jsonContent['included'])
    df=df[df['$type']=='com.linkedin.voyager.dash.identity.profile.Position']
    df['startMonth']=df['dateRange'].map(lambda x:x['start']['month'])
    df['startYear']=df['dateRange'].map(lambda x:x['start']['year'])
    df.sort_values(by=['startYear', 'startMonth'],ascending=False,inplace=True)
    firstName=nameBlock.iloc[0]['firstName']
    lastName=nameBlock.iloc[0]['lastName']
    Title=df.iloc[0]['title'] if df.iloc[0]['title'] else None
    CompanyName=df.iloc[0]['companyName'] if df.iloc[0]['companyName'] else None
    Title1=df.iloc[1]['title'] if df.iloc[1]['title'] else None
    CompanyName1=df.iloc[1]['companyName'] if df.iloc[1]['companyName'] else None
    return firstName,lastName,Title,CompanyName,Title1,CompanyName1,url

def get_cookie():
    if os.path.exists(os.path.join(os.getcwd(), "cookie", 'session.csv')) is True:
        df=pd.read_csv(os.path.join(os.getcwd(), "cookie", 'session.csv'))
    else:
        df=Login()
    return df

def crawl(url):
    memberId=url.split('/')[-1]
    params = (
        ('q', 'memberIdentity'),
        ('memberIdentity', str(memberId)),
        ('decorationId', 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-73'),
        )
    cookie=get_cookie()
    headers=get_Headers(cookie)
    response = requests.get('https://www.linkedin.com/voyager/api/identity/dash/profiles', headers=headers, params=params)
    contact=Extract_Contact(response.text,url)
    print(contact)