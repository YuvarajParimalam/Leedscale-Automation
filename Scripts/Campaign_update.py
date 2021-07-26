import requests
from bs4 import BeautifulSoup
import pandas as pd
import configparser
import os
import time,random
from urllib.parse import quote
from Lolagroove import Get_Data_Params,save_as_dataframe
from tools.log_script import log_file_write
from temp import get_form_data_campaign
config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
UserName=config.get('Lolagroove','UserName')
PassWord=config.get('Lolagroove','PassWord')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
params = (
    ('ReturnUrl', '/Admin/CampaignListing.aspx?rpp=1000'),
    ('rpp', '1000'),
    ('AspxAutoDetectCookieSupport', '1'),
)

def get_form_data(key,row):
  formdata = [
    ('k', key.replace('"','')),
    ('t', 'json'),
    ('a', 'ud'),
    ('vid', str(row['ID'])),
    ('uid', '1449'),
    ('d[fieldNames][]', 'firstname'),
    ('d[fieldNames][]', 'lastname'),
    ('d[fieldValues][]', row['First Name']),
    ('d[fieldValues][]', row['Last Name']),
    ('rv', 'false'),
  ]
  return formdata

with requests.Session() as s:
        data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'txtInput': UserName,
        'txtPassword': PassWord,
        'lnkBtnLogin': 'Login'
        }
        page = s.get('https://v3.lolagrove.com/admin/login.aspx?ReturnUrl=%2fAdmin%2fCampaignListing.aspx%3frpp%3d1000&rpp=1000')
        time.sleep(2)
        soup = BeautifulSoup(page.text,'html.parser')
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        response = s.post('https://v3.lolagrove.com/admin/login.aspx', headers=headers, params=params, data=data)
        time.sleep(3)
        htmlContent=BeautifulSoup(response.text,'html.parser')
        next_url='https://v3.lolagrove.com/Admin/CampaignEyeballing.aspx?id=16852'
        page = s.get(next_url,headers=headers)
        print(page.status_code)
        time.sleep(2)
        soup = BeautifulSoup(page.content,'html.parser')
        data = Get_Data_Params(soup)
        response = s.post(next_url, headers=headers, data=data)
        AuthKey=response.text.split('function GetAuthenticationKey() {')[1].split('}')[0].replace('return','').replace(';','').replace("'",'').strip()
        # df=save_as_dataframe(response.text)
        df=pd.read_excel('campaign.xlsx')
        df=df.fillna(value='')
        for i in range(1):
          row=df.iloc[i]          
          formdata=get_form_data_campaign(AuthKey,row) 
          response = s.post('https://v3.lolagrove.com/scrubbing.ashx', headers=headers, data=formdata)
          with open('temp.json','a',encoding='utf-8') as f:
            f.write(response.text)
