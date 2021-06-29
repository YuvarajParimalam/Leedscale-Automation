import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
import os
import pandas as pd

headers = {
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}

def MSN_Scraper(company,Domain):
    company=company+' '+Domain
    query=quote(company)
    response = requests.get('https://www.bing.com/search?q={}'.format(str(query)), headers=headers)
    print(response.status_code)
    data=soup(response.text,'html.parser')
    try:
        url=data.find('h2').find('a')['href']
    except:
        url=''
    return url
