url='https://www.owler.com/company/intrinsec'

import requests
from bs4 import BeautifulSoup as soup
import configparser
import os
from tools.log_script import log_file_write

config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
proxy = config.get('Proxy', 'Proxy')
proxies = {"http":'http://'+proxy, "https":'http://'+proxy}



headers = {
    'authority': 'www.zoominfo.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-US,en;q=0.9',
   }

def owler_scraper(url):
    print('inside owler')
    try:
        response= requests.get(url,headers=headers,proxies=proxies)        
        log_file_write(id,'owler response'+str(response.status_code))
        data=soup(response.text,'html.parser') 
        try:
            company=data.find('h1',class_='company-name').text.strip()
        except:
            company=''
        try:
            Revenue=data.find('div',class_='count-container REVENUE_EXACT CP botifyrevenuedata').text.strip()
        except:
            Revenue=''
        contact={
            'Owler_company':company,
            'Owler_Revenue':Revenue,
            'Owler_Link':url
        }
        return contact
    except Exception as e:
        log_file_write(id,'owler error'+str(e))
        contact={
                'Owler_company':'',
                'Owler_Revenue':'',
                'Owler_Link':''
            }
        return contact




