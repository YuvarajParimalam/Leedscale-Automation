
from tools.log_script import log_file_write
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
from tools.log_script import log_file_write
import os
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

def scrape(url):
    r=requests.get(url,headers=headers)
    data=soup(r.text,'html.parser')
    print(r.status_code)
    if r.status_code==200:
      return data
    else:
      return ''

def countwords(description,address):
    count=0
    words=address.split(' ')
    for word in words:
        if str(word).lower() in description.lower():
            count=count+1
    return float(count/len(words))

def extract_details(source,address1,company,Postal,searchEngine):
    try:
        Google_Results=[]
        if searchEngine=='Google':
            for atag in source.findAll('div',class_='tF2Cxc'):
                try:
                    LinkURL=atag.find('div',class_='yuRUbf').find('a')['href']
                except:
                    LinkURL=''
                try:
                    LinkText=atag.find('div',class_='yuRUbf').find('h3').text.strip()
                except:
                    LinkText=''
                try:
                    LinkDiscription=atag.find('div',class_='IsZvec').text.strip()
                except:
                    LinkDiscription=''
                detail={
                    'LinkURL':LinkURL,
                    'LinkText':LinkText,
                    'LinkDiscription':LinkDiscription,
                }
                Google_Results.append(detail)
        else:
            for atag in source.findAll('li',class_='b_algo'):
                try:
                    LinkURL=atag.find('a')['href']
                except:
                    LinkURL=''
                try:
                    LinkText=atag.find('h2').text.strip()
                except:
                    LinkText=''
                try:
                    LinkDiscription=atag.find('div',class_='b_caption').find('p').text.strip()
                except:
                    LinkDiscription=''
                detail={
                    'LinkURL':LinkURL,
                    'LinkText':LinkText,
                    'LinkDiscription':LinkDiscription,
                }
                Google_Results.append(detail)  
        for i in range(len(Google_Results)):
            total=countwords(Google_Results[i]['LinkDiscription'],address1)
            Google_Results[i]['Total']=total
        result_data=[]
        for i in range(len(Google_Results)):
            if company.lower() in Google_Results[i]['LinkDiscription'].lower() and str(Postal.lower()) in Google_Results[i]['LinkDiscription'].lower().replace(' ',''):
                result_data.append(Google_Results[i])
        if len(result_data)>1: 
            df=pd.DataFrame(result_data)
            df.sort_values(by='Total',ascending=False)
            addressLink=df.iloc[0]['LinkURL']
            addressDetail={
                'addressLink':addressLink,
                'accuracy':df.iloc[0]['Total'],
                'Text':df.iloc[0]['LinkDiscription']

            }
        else:
            addressDetail={
                'addressLink':'',
                'accuracy':'',
                'Text':''
            }
        return addressDetail
    except Exception as e:
        log_file_write('','error in getting address'+str(e))

def Main(address1,country,Postal,company,searchEngine,city=None,):
    query=quote(address1+' '+city+' '+Postal+' '+country+' '+company)
    if searchEngine=='Google':
        url='https://www.google.com/search?q='+str(query)
    else:
        url='https://www.bing.com/search?q='+str(query)
    result=scrape(url)
    if result:
        evidence=extract_details(result,address1,company,Postal,searchEngine)
    return evidence
