import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import configparser
import os
import time,random
pd.options.mode.chained_assignment = None

from Google_Search import Search_Contact
from Linkedin import crawl,FetchLinkedinLink
from tools.utiltity import file_cleanup,CheckDomain
from Zoominfo import Zoominfo_scraper
from company_matching import match_company_name

actualdate=datetime.datetime.now().strftime("%d/%m/%Y")
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


def Lolagroove():
    df2=pd.DataFrame()
    with requests.Session() as s:
        data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'txtInput': UserName,
        'txtPassword': PassWord,
        'lnkBtnLogin': 'Login'
        }
        input='Adobe_Customer_Intelligence_Q2_FY21 4 (Allchecks)'
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
        page = s.get(next_url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        data = Get_Data_Params(soup)
        response = s.post(next_url, headers=headers, data=data)
        df=save_as_dataframe(response.text)
        outputPath=os.path.join(os.getcwd(),'Output')
        save_as_csv(outputPath+'/'+input,df)
        return df

# df=Lolagroove()
# file_cleanup()
outputPath=os.path.join(os.getcwd(),'Output')
df=pd.read_csv(os.path.join(outputPath,'Adobe_Customer_Intelligence_Q2_FY21 4 (Allchecks).csv'))
New_Data=[]
for i in range(1):
    row=df.iloc[i]
    #get zoominfo URL 
    zoominfo_url=Search_Contact(row,'Zoominfo') # return first url from google search for zoominfo
    zoominfoData=Zoominfo_scraper(zoominfo_url) #Extract Revenue and Emp Size
    # Extract Linkedin URL Based on First Name , Last Name, Jobtitle and Company from LInkedin
    try:
        linkedinurl=FetchLinkedinLink(row)
        linkedinurl=linkedinurl.split('?')[0]
    except:
        linkedinurl=Search_Contact(row,'Linkedin') # return first url from google search for Linkedin
        
    # get data from linkedin based on url scraped from Linkedin and Google Search
    if 'linkedin.com/in' in linkedinurl:
        LinkedinData=crawl(linkedinurl,row['ID'])
        print(LinkedinData)
    else:
        print('not ablt to locate Linkedin URL')
    try:
        company_match_status=match_company_name(row['Company Name'] ,LinkedinData['CompanyName'] ,searchMethod= None)
    except:
        company_match_status=''
    try:
        Zoominfo_company_match_status=match_company_name(row['Company Name'] ,zoominfoData['company'] ,searchMethod= None)
    except:
        Zoominfo_company_match_status=''
    try:
        DomainStatus=CheckDomain(row['Email'],LinkedinData['linkedinCompanyWebsite'])
    except Exception as e:
        print('unable to find the domain status',e)

    #update the scraped data to the existing file
    row['zoominfo_company'] = zoominfoData['company'],   
    row['zoominfo_revenue'] = zoominfoData['Revenue'],
    row['zoominfoEmployees'] = zoominfoData['Employees'],
    row['linkedinfirstName'] = LinkedinData['firstName'],
    row['linkedinlastName'] = LinkedinData['lastName'],
    row['linkedinTitle'] = LinkedinData['Title'],
    row['linkedinCompanyName'] = LinkedinData['CompanyName'],
    row['LinkedinContacturl'] = LinkedinData['LinkedinContacturl'],
    row['LinkedinCompanyURL'] = LinkedinData['LinkedinCompanyURL'],
    row['linkedinCompanyEmpSize'] = LinkedinData['linkedinCompanyEmpSize'],
    row['linkedinCompanyWebsite'] = LinkedinData['linkedinCompanyWebsite'],
    row['zoominfo_url']=zoominfo_url,
    row['Linkedin_company_match_status'] = company_match_status,
    row['Zoominfo_company_match_status'] = Zoominfo_company_match_status,
    row['LinkedinDomainStatus']=DomainStatus

    New_Data.append(row)

new_df=pd.DataFrame(New_Data)
new_df.to_csv('Final_Data.csv')






