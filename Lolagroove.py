import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import configparser
import os
actualdate=datetime.datetime.now().strftime("%d/%m/%Y")

from Google_Search import Search_Contact
from Linkedin import crawl

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


def Get_Data_Params(soup): 
    curdate=soup.select_one("#AreaContentHolder_ContentArea_ddlScrubbingDate").findAll('option')[1]['value']
    data = {
      '__EVENTTARGET': '',
      '__EVENTARGUMENT': '',
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlStatus': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnStatus': '0',
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlScrubbingDate': str(curdate),
      'ctl00$ctl00$AreaContentHolder$ContentArea$hdnDate': str(curdate),
      'ctl00$ctl00$AreaContentHolder$ContentArea$ddlRecords': '100',
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


def save_as_csv(table_name, table_headers,rows):
    df=pd.DataFrame(rows,columns=table_headers)
    df.to_csv(f"{table_name}.csv",index=False)
    return df

def Lolagroove():
    with requests.Session() as s:
        data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'txtInput': UserName,
        'txtPassword': PassWord,
        'lnkBtnLogin': 'Login'
        }
        input='Adobe_AES_Pilot_Q2_FY21 4 (Allchecks)'
        page = s.get('https://v3.lolagrove.com/admin/login.aspx?ReturnUrl=%2fAdmin%2fCampaignListing.aspx%3frpp%3d1000&rpp=1000')
        soup = BeautifulSoup(page.text,'html.parser')
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        response = s.post('https://v3.lolagrove.com/admin/login.aspx', headers=headers, params=params, data=data)
        htmlContent=BeautifulSoup(response.text,'html.parser')
        for page_url in htmlContent.findAll('table')[1].findAll('td'):
            try: 
                if page_url.find('a').text==input:
                    next_url='https://v3.lolagrove.com'+page_url.find('a')['href']
            except: 
                pass
        page = s.get(next_url)
        soup = BeautifulSoup(page.content,'html.parser')
        data = Get_Data_Params(soup)
        response = s.post(next_url, headers=headers, data=data)
        htmlContent=BeautifulSoup(response.text,'html.parser')
        tableData=htmlContent.findAll('table')[1]
        head = get_table_headers(tableData)
        table_rows = get_table_rows(tableData)
        df=save_as_csv(input, head,table_rows)
        return df
df=pd.read_csv('Adobe_AES_Pilot_Q2_FY21 4 (Allchecks).csv')
url=Search_Contact(df.iloc[0])
Evidence=crawl(url)
print(Evidence)
