import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import configparser
import os
from urllib.parse import quote

actualdate=datetime.datetime.now().strftime("%d/%m/%Y")
config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
UserName=config.get('Lolagroove','UserName')
PassWord=config.get('Lolagroove','PassWord')
Date=config.get('CampaignDate','Date')
URL=config.get('Lolagroove','URL')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}

params = (
    ('ReturnUrl', '/Admin/CampaignListing.aspx?rpp=1000'),
    ('rpp', '1000'),
    ('AspxAutoDetectCookieSupport', '1'),
)

params2 = (
    ('dt', '29/07/2021'),
    ('s', '0'),
    ('pid', '0'),
    ('sid', '0'),
    ('m', '1000'),
    ('p', '3'),
)


def Get_Data_Params(soup): 
    curdate=soup.select_one("#AreaContentHolder_ContentArea_ddlScrubbingDate").findAll('option')[1]['value']
    data = {
      '__EVENTTARGET': '',
      '__EVENTARGUMENT': '',
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlStatus': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnStatus': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlScrubbingDate': str(Date),
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnDate': str(Date),
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlRecords': '1000',
      'ctl00$ctl00$AreaContentHolder$ContentArea$btnShowData': 'Show Data',
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnSite': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnPlacement': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnRowIndexes': '',
      'address1': '',
      'address2': '',
      'address3': '',
      'address4': '',
      'address5': '',
      'towncity': '',
      'state': '',
      'postcode': ''
    }
    data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
    data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
    data["__PREVIOUSPAGE"] = soup.select_one("#__PREVIOUSPAGE")["value"]
    return data

def get_table_headers(table):
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    headers[0], headers[1]='emailStatus','ID'
    return headers


def get_table_rows(table):    
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        tds = tr.find_all("td")
        if len(tds) == 0:
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            emailstatus=tds[3]['emailstatus']
            if int(emailstatus)==70:
                emailstatus='valid'
            elif int(emailstatus)==8258:
                emailstatus='invalid'
            else:
                emailstatus='-'
            id=tds[2].find('input')['name'].split('_')[1]
            for td in tds:                
                cells.append(td.text.strip())
            cells[0]=emailstatus
            cells[1]=id
        rows.append(cells)
    return rows


def save_as_csv(table_name, df):
    df.to_csv(f"{table_name}.csv",index=False)


def save_as_dataframe(source):
    htmlContent=BeautifulSoup(source,'html.parser')
    tableData=htmlContent.findAll('table')[1]
    head = get_table_headers(tableData)
    table_rows = get_table_rows(tableData)
    df=pd.DataFrame(table_rows,columns=head)
    return df


def Lolagroove(campaign):
    with requests.Session() as s:
        data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'txtInput': UserName,
        'txtPassword': PassWord,
        'lnkBtnLogin': 'Login'
        }
        page = s.get('https://v3.lolagrove.com/admin/login.aspx?ReturnUrl=%2fAdmin%2fCampaignListing.aspx%3frpp%3d1000&rpp=1000')
        print(page.status_code)
        soup = BeautifulSoup(page.text,'html.parser')
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        response = s.post('https://v3.lolagrove.com/admin/login.aspx', headers=headers, params=params, data=data)
        print(response.status_code)
        next_url=URL
        print(next_url)
        page = s.get(next_url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        data = Get_Data_Params(soup)
        page = s.post(next_url, headers=headers, data=data)
        print(page.status_code)
        df=save_as_dataframe(page.text)
        try:
            df['lead_creation_month']=df['lead_creation_month'].apply(lambda x:"'"+x)
            df['lead_creation_day']=df['lead_creation_day'].apply(lambda x:"'"+x)
        except:
            pass
        try:
            df['Sub_id']=df['Sub_id'].apply(lambda x:"'"+x)
        except:
            pass
        outputPath=os.path.join(os.getcwd(),'Output')
        save_as_csv(outputPath+'/'+campaign,df)
        return df







