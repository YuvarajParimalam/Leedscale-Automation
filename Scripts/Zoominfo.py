import requests
from bs4 import BeautifulSoup as soup
import configparser
import os
import time,random
from tools.log_script import log_file_write

config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
proxy = config.get('Proxy', 'Proxy')
proxies = {"http":'http://'+proxy, "https":'http://'+proxy}



headers = {
    'authority': 'www.zoominfo.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_pxvid=fdce47f0-ad9c-11eb-827e-0173befe990c; _rdt_uuid=1620217538189.9ef8617b-fc40-4aac-837e-28279667c6e5; _ga=GA1.2.1323912197.1620217538; cf_clearance=806f6d36dca1ad8f4291189751832a8cc333bab6-1625745802-0-150; _mibhv=anon-1625745857716-3596812425_8799; _gcl_au=1.1.1048507995.1628742555; _gid=GA1.2.1869302026.1628742555; pxcts=d664bce0-fb25-11eb-96ee-cf8aebb26cee; _pxhd=Uj8jzqsqlP0qV/6pjSH/IDfQutF5NDeytqP1IYtCdJdLw7oFlG9BUJQHAWKY3E8GJ7AO6H6uI83usozzLUCNww; amplitude_id_14ff67f4fc837e2a741f025afb61859czoominfo.com=eyJkZXZpY2VJZCI6IjhjZjc2OTk2LWFkZmMtNDlhNC04N2I4LTgwYWZlMzgxNzI1MFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYyODc0MjU1NDY0OCwibGFzdEV2ZW50VGltZSI6MTYyODc0MjU2MDU1NiwiZXZlbnRJZCI6MTUsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjoxNX0=',
}

def Zoominfo_scraper(url,id):
    print('inside zoominfo')
    try:
        for _ in range(5):
            response= requests.get(url,headers=headers,proxies=proxies)
            if response.status_code==200:
                time.sleep(5)
                print('got response.from zoomfino')
                break
        
        log_file_write(id,'zooinfo response'+str(response.status_code))
        data=soup(response.text,'html.parser') 
        try:
            company=data.find('h1',class_='company-name').text.strip()
        except:
            company=''
        try:
            Revenue=[x.text for x in data.findAll('app-icon-text') if 'Revenue' in x.text][0]
            Revenue=Revenue.replace('Revenue:','')
        except:
            Revenue=''
        try:
            Employees=[x.text for x in data.findAll('app-icon-text') if 'Employees' in x.text][0]
            Employees=Employees.replace('Employees:','')
        except:
            Employees=''
        contact={
            'company':company,
            'Revenue':Revenue,
            'Employees':Employees
        }
        return contact
    except Exception as e:
        log_file_write(id,'zooinfo error'+str(e))
        contact={
                'company':'',
                'Revenue':'',
                'Employees':''
            }
        return contact





