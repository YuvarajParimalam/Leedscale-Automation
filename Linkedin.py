import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import time
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
    time.sleep(20)
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
def Extract_Contact(source,url,ID,headers):
    try:
        jsonContent=json.loads(source)
        nameBlock=pd.DataFrame(jsonContent['included'])
        nameBlock=nameBlock[nameBlock['$type']=='com.linkedin.voyager.dash.identity.profile.Profile']
        df=pd.DataFrame(jsonContent['included'])
        try:
            curPath=os.path.join(os.getcwd(),'Linkedin_Output')
            df.to_csv(curPath+'/{}.csv'.format(str(ID)))
        except Exception as e:
            print('unable to write to file',e)
        df=df[df['$type']=='com.linkedin.voyager.dash.identity.profile.Position']
        tempCompanyURN=df.iloc[0]['companyUrn']
        def get_Month(x):
            try:
                month=x['start']['month']
            except:
                month=0
            return month
        def get_Year(x):
            try:
                year=x['start']['year']
            except:
                year=0
            return year
        df['startMonth']=df['dateRange'].apply(get_Month)
        df['startYear']=df['dateRange'].apply(get_Year)
        df.sort_values(by=['startYear', 'startMonth'],ascending=False,inplace=True)
        df.fillna(0,inplace=True)
        CompanyURN=df.iloc[0]['*company']
        if CompanyURN == 0:
            CompanyURN=df.iloc[1]['*company']
        if CompanyURN==0:
            CompanyURN=tempCompanyURN
        firstName=nameBlock.iloc[0]['firstName']
        lastName=nameBlock.iloc[0]['lastName']
        Title=df.iloc[0]['title']
        CompanyName=df.iloc[0]['companyName']
        Title1=df.iloc[1]['title'] 
        CompanyName1=df.iloc[1]['companyName'] 
        df2=pd.DataFrame(jsonContent['included'])
        df2=df2[df2['entityUrn']==CompanyURN]
        LinkedinCompanyEvidenceURL=df2.iloc[0]['url']
        companyID=CompanyURN.split(':')[-1]
        linkedinCompanyEmpSize,linkedinCompanyWebsite=Fetch_Company_Evidence(companyID,headers)
        contact={
            'firstName':firstName,
            'lastName':lastName,
            'Title':Title,
            'CompanyName':CompanyName,
            'Title1':Title1,
            'CompanyName1':CompanyName1,
            'LinkedinContacturl':url,
            'LinkedinCompanyURL':LinkedinCompanyEvidenceURL,
            'linkedinCompanyEmpSize':linkedinCompanyEmpSize,
            'linkedinCompanyWebsite':linkedinCompanyWebsite,
        }
        return contact
    except Exception as e:
        contact={
            'firstName':'',
            'lastName':'',
            'Title':'',
            'CompanyName':'',
            'Title1':'',
            'CompanyName1':'',
            'LinkedinContacturl':url,
            'LinkedinCompanyURL':'',
            'linkedinCompanyEmpSize':'',
            'linkedinCompanyWebsite':'',
        }
        print('Error in extracting contact from Linkedin',e)
        return contact

#cookie generation from dataframe        
def get_cookie():
    try:
        if os.path.exists(os.path.join(os.getcwd(), "cookie", 'session.csv')) is True:
            df=pd.read_csv(os.path.join(os.getcwd(), "cookie", 'session.csv'))
        else:
            df=Login()
        return df
    except Exception as e:
        print('error occured while getting cookie',e)

#function to get linkedinURL from LInkedin
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

def Fetch_Company_Evidence(CompanyID,headers):
    params = (
            ('decorationId', 'com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-35'),
            ('q', 'universalName'),
            ('universalName', str(CompanyID)),
        )
    response = requests.get('https://www.linkedin.com/voyager/api/organization/companies', headers=headers, params=params)
    data=json.loads(response.text)
    for types in data['included']:
        try:
            staff=types['staffCountRange']
        except:
            pass
        try:
            website=types['companyPageUrl']
        except:
            pass
    try:
        employeeSize=staff['start']
        try:
            end=staff['end']
        except:
            end=''
        employeeSize=str(employeeSize)+'-'+str(end)
    except:
        employeeSize=''
    try:
        website=website
    except:
        website=''
    return (employeeSize,website)

#Linkedin Scraping Starts Here
def crawl(url,ID):
    memberId=url.split('/')[-1]
    if 'miniProfile' in url:
        memberId=url.split('?')[0].split('/')[-1]
    if len(memberId)==2 or '=' in memberId:
        memberId=url.split('/')[-2]
    params = (
        ('q', 'memberIdentity'),
        ('memberIdentity', str(memberId)),
        ('decorationId', 'com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-73'),
        )
    cookie=get_cookie()
    headers=get_Headers(cookie)
    response = requests.get('https://www.linkedin.com/voyager/api/identity/dash/profiles', headers=headers, params=params)
    contact=Extract_Contact(response.text,url,ID,headers)
    return contact