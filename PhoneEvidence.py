
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
import re
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

def clean_telephone(telephone):
    if telephone:
        telephone = (
            telephone.replace(" ", "")
            .replace(".", "")
            .replace(")", "")
            .replace("(", "")
            .replace("-", "")
            .replace("+", "")
            .strip()
        )
        if re.findall(r'\d+',telephone):
           telephone = re.findall(r'\d+',telephone)[0]
        if len(telephone) == 12:
            telephone = telephone[2:]
        return telephone

def extract_details(source,phone,company,searchEngine):
    Google_Results=[]
    if searchEngine=='Google':
        for atag in source.findAll('div',class_='tF2Cxc'):
            try:
                LinkURL=atag.find('div',class_='yuRUbf').find('a')['href']
            except:
                LinkURL=''
            try:
                LinkDiscription=atag.find('div',class_='IsZvec').text.strip()
            except:
                LinkDiscription=''
            detail={
                'LinkURL':LinkURL,
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
                LinkDiscription=atag.find('div',class_='b_caption').find('p').text.strip()
            except:
                LinkDiscription=''
            detail={
                'LinkURL':LinkURL,
                'LinkDiscription':LinkDiscription,
            }
            Google_Results.append(detail)  
    result_data=[]
    for i in range(len(Google_Results)):
        if company.lower() in Google_Results[i]['LinkDiscription'].lower() and str(clean_telephone(phone)) in Google_Results[i]['LinkDiscription'].replace(' ',''):
            result_data.append(Google_Results[i])
    try:
        phoneEvidence=result_data[0]['LinkURL']
    except:
        phoneEvidence=''
    return phoneEvidence

def PhoneValidation(phone,company,searchEngine):
    query=quote(phone+' '+company)
    if searchEngine=='Google':
        url='https://www.google.com/search?q='+str(query)
    else:
        url='https://www.bing.com/search?q='+str(query)
    result=scrape(url)
    if result:
        evidence=extract_details(result,phone,company,searchEngine)
    return evidence
