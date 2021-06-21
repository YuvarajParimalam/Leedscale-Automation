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
from urllib.parse import quote

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
    time.sleep(40)
    df=pd.DataFrame(driver.get_cookies())
    filePath=os.path.join(os.getcwd(),'cookie')
    df.to_csv(filePath+'/session.csv')
    driver.quit()
    return df

#extract headers from session sookie
def get_Headers(df):
    li_at=df.loc[df['name'] == 'li_at', 'value'].item()
    jsession=df.loc[df['name'] == 'JSESSIONID', 'value'].item()
    cookie='JSESSIONID='+str(jsession)+'; li_at='+str(li_at)+';'
    headers = {
    'authority': 'www.linkedin.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'x-restli-protocol-version': '2.0.0',
    'x-li-lang': 'en_US',
    'sec-ch-ua-mobile': '?0',
    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_all;Y75xNYzsR1m2fxt6mvvTUA==',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': str(jsession).replace('"',''),
    'x-li-track': '{"clientVersion":"1.8.6979","mpVersion":"1.8.6979","osName":"web","timezoneOffset":5.5,"timezone":"Asia/Calcutta","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1366,"displayHeight":768}',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.linkedin.com/in/richard-hall-36b64a31/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': str(cookie)
  }
    return headers

#Extract Contact from Linkedin URL
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

def FetchLinkedinLink(row):
    cookie=get_cookie()
    headers=get_Headers(cookie)
    companydetail=row['First Name']+" "+row['Last Name']+" "+row['Job Title']+" "+row['Company Name'].split(' ')[0]
    input=quote(companydetail, safe='')
    response = requests.get('https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-112&origin=TYPEAHEAD_ESCAPE_HATCH&q=all&query=(keywords:{0},flagshipSearchIntent:SEARCH_SRP,queryParameters:(resultType:List(ALL)),includeFiltersInResponse:false)&start=0'.format(str(input)), headers=headers)
    data=json.loads(response.text)
    linkedinLink=data['data']['elements'][0]['featureUnion']['heroEntityCard']['navigationUrl']
    print(linkedinLink)
    return linkedinLink



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
    return contact