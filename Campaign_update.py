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
    ('d[fieldNames][]', 'meritleadid'),
    ('d[fieldNames][]', 'email'),
    ('d[fieldNames][]', 'email_evidence'),
    ('d[fieldNames][]', 'telephone'),
    ('d[fieldNames][]', 'phone_evidence'),
    ('d[fieldNames][]', 'address1'),
    ('d[fieldNames][]', 'towncity'),
    ('d[fieldNames][]', 'postcode'),
    ('d[fieldNames][]', 'country'),
    ('d[fieldNames][]', 'address_evidence'),
    ('d[fieldNames][]', 'firstname'),
    ('d[fieldNames][]', 'lastname'),
    ('d[fieldNames][]', 'linkedin_id_url'),
    ('d[fieldNames][]', 'jobtitle'),
    ('d[fieldNames][]', 'jobtitle_evidence'),
    ('d[fieldNames][]', 'job_function'),
    ('d[fieldNames][]', 'companyname'),
    ('d[fieldNames][]', 'company_url'),
    ('d[fieldNames][]', 'industry'),
    ('d[fieldNames][]', 'company_evidence'),
    ('d[fieldNames][]', 'company_size'),
    ('d[fieldNames][]', 'companysize_evidence'),
    ('d[fieldNames][]', 'turnover'),
    ('d[fieldNames][]', 'turnover_evidence'),
    ('d[fieldNames][]', 'supplier_lead_id'),
    ('d[fieldNames][]', 'asset_title'),
    ('d[fieldNames][]', 'rejection_evidence'),
    ('d[fieldNames][]', 'useragent'),
    ('d[fieldNames][]', 'lead_creation_date'),
    ('d[fieldNames][]', 'tactic'),
    ('d[fieldNames][]', 'source'),
    ('d[fieldNames][]', 'sub_source'),
    ('d[fieldNames][]', 'update_date'),
    ('d[fieldNames][]', 'input_placement'),
    ('d[fieldNames][]', 'secure'),
    ('d[fieldNames][]', 'lead_type'),
    ('d[fieldNames][]', 'lead_creation_day'),
    ('d[fieldNames][]', 'lead_creation_month'),
    ('d[fieldNames][]', 'lead_creation_year'),
    ('d[fieldNames][]', 'sub_id'),
    ('d[fieldNames][]', 'callback_id'),
    ('d[fieldValues][]', row['ID']),
    ('d[fieldValues][]', row['Email']),
    ('d[fieldValues][]', row['email_evidence']),
    ('d[fieldValues][]', row['Telephone']),
    ('d[fieldValues][]', row['phone_evidence']),
    ('d[fieldValues][]', row['Address 1']),
    ('d[fieldValues][]', row['Town/City']),
    ('d[fieldValues][]', row['Postal/Zip Code']),
    ('d[fieldValues][]', row['Country']),
    ('d[fieldValues][]', row['address_evidence']),
    ('d[fieldValues][]', row['First Name']),
    ('d[fieldValues][]', row['Last Name']),
    ('d[fieldValues][]', row['linkedin_id_url']),
    ('d[fieldValues][]', row['Job Title']),
    ('d[fieldValues][]', row['jobtitle_evidence']),
    ('d[fieldValues][]', row['job_function']),
    ('d[fieldValues][]', row['Company Name']),
    ('d[fieldValues][]', row['company_url']),
    ('d[fieldValues][]', row['Industry']),
    ('d[fieldValues][]', row['company_evidence']),
    ('d[fieldValues][]', row['company_size']),
    ('d[fieldValues][]', row['companysize_evidence']),
    ('d[fieldValues][]', row['turnover']),
    ('d[fieldValues][]', row['turnover_evidence']),
    ('d[fieldValues][]', row['Supplier Lead ID']),
    ('d[fieldValues][]', row['asset_title']),
    ('d[fieldValues][]', row['rejection_evidence']),
    ('d[fieldValues][]', row['User Agent']),
    ('d[fieldValues][]', row['lead_creation_date']),
    ('d[fieldValues][]', row['tactic']),
    ('d[fieldValues][]', row['Source']),
    ('d[fieldValues][]', row['sub_source']),
    ('d[fieldValues][]', row['update_date']),
    ('d[fieldValues][]', row['input_placement']),
    ('d[fieldValues][]', row['secure']),
    ('d[fieldValues][]', row['lead_type']),
    ('d[fieldValues][]', row['lead_creation_day']),
    ('d[fieldValues][]', row['lead_creation_month']),
    ('d[fieldValues][]', row['lead_creation_year']),
    ('d[fieldValues][]', row['Sub_id']),
    ('d[fieldValues][]', row['Callback_id']),
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
        for i in range(6,15):
          row=df.iloc[i]          
          formdata=get_form_data_campaign(AuthKey,row) 
          response = s.post('https://v3.lolagrove.com/scrubbing.ashx', headers=headers, data=formdata)
          with open('temp.json','a',encoding='utf-8') as f:
            f.write(response.text)
          time.sleep(random.randint(2,6))