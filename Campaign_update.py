import requests
from bs4 import BeautifulSoup
import pandas as pd
import configparser
import os
import time
from urllib.parse import quote
from Lolagroove import Get_Data_Params

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

def get_form_data(key):
  formdata = [
    ('k', key.replace('"','')),
    ('t', 'json'),
    ('a', 'ud'),
    ('vid', '518622247'),
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
    ('d[fieldValues][]', '518622247'),
    ('d[fieldValues][]', 'raj.singh-dehal@centerparcs.co.uk'),
    ('d[fieldValues][]', 'Email evidence not found'),
    ('d[fieldValues][]', '44 1623 821600'),
    ('d[fieldValues][]', 'Phone evidence not found'),
    ('d[fieldValues][]', 'One Edison Rise|| New Ollerton'),
    ('d[fieldValues][]', 'Darlton'),
    ('d[fieldValues][]', 'NG229DP'),
    ('d[fieldValues][]', 'United Kingdom'),
    ('d[fieldValues][]', 'Address evidence not found'),
    ('d[fieldValues][]', 'Raj'),
    ('d[fieldValues][]', 'Singh-dehal'),
    ('d[fieldValues][]', 'https://www.linkedin.com/in/raj-singh-dehal-095a839b/'),
    ('d[fieldValues][]', 'Chief Corporate Officer'),
    ('d[fieldValues][]', 'https://www.linkedin.com/in/raj-singh-dehal-095a839b/'),
    ('d[fieldValues][]', '- Function-'),
    ('d[fieldValues][]', 'Center Parcs'),
    ('d[fieldValues][]', 'centerparcs.co.uk'),
    ('d[fieldValues][]', 'Sport & Leisure'),
    ('d[fieldValues][]', 'https://www.linkedin.com/company/centerparcs/about/'),
    ('d[fieldValues][]', '5001-10000'),
    ('d[fieldValues][]', 'https://www.linkedin.com/company/centerparcs/about/'),
    ('d[fieldValues][]', '$25.1m - $1b'),
    ('d[fieldValues][]', 'https://www.owler.com/company/centerparcs'),
    ('d[fieldValues][]', 'MAJTAL_212'),
    ('d[fieldValues][]', 'A Legality Guide To Esignature'),
    ('d[fieldValues][]', 'Non-spec Asset Matrix (Job Function mismatch)'),
    ('d[fieldValues][]', 'Uday Sankar'),
    ('d[fieldValues][]', '07/12/2020'),
    ('d[fieldValues][]', 'email'),
    ('d[fieldValues][]', 'test'),
    ('d[fieldValues][]', 'Benchmark'),
    ('d[fieldValues][]', '7/7/2021 4:11:55 PM'),
    ('d[fieldValues][]', 'DS_Docusign - Merit Automation Test_76103'),
    ('d[fieldValues][]', 'DocuSign_DocuSign_EMEA-N_FY21_Q4'),
    ('d[fieldValues][]', 'UK MAJ TAL'),
    ('d[fieldValues][]', '07'),
    ('d[fieldValues][]', '12'),
    ('d[fieldValues][]', '2020'),
    ('d[fieldValues][]', '76103.20009'),
    ('d[fieldValues][]', '518597864'),
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
        soup = BeautifulSoup(page.text,'html.parser')
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        response = s.post('https://v3.lolagrove.com/admin/login.aspx', headers=headers, params=params, data=data)
        htmlContent=BeautifulSoup(response.text,'html.parser')
        next_url='https://v3.lolagrove.com/Admin/CampaignEyeballing.aspx?id=16852'
        page = s.get(next_url,headers=headers)
        print(page.status_code)
        time.sleep(2)
        soup = BeautifulSoup(page.content,'html.parser')
        data = Get_Data_Params(soup)
        response = s.post(next_url, headers=headers, data=data)
        AuthKey=response.text.split('function GetAuthenticationKey() {')[1].split('}')[0].replace('return','').replace(';','').replace("'",'').strip()
        formdata=get_form_data(AuthKey)
        response = s.post('https://v3.lolagrove.com/scrubbing.ashx', headers=headers, data=formdata)
