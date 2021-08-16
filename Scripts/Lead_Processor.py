
import pandas as pd
import os,configparser
pd.options.mode.chained_assignment = None


from Scripts.Google_Search import Search_Contact
from Scripts.Linkedin import crawl,FetchLinkedinLink
from tools.utiltity import CheckDomain
from Scripts.Zoominfo import Zoominfo_scraper
from Scripts.company_matching import match_company_name
from Scripts.AddressEvidence import Main
from Scripts.PhoneEvidence import PhoneValidation
from Scripts.owler import owler_scraper
from tools.log_script import log_file_write

df=pd.read_excel('LinkedIn Industries Match.xlsx')
LinkedIn_Industry=list(df['LinkedIn Industry'])
lolagroove_Industry=list(df['Lolagrove'])

config = configparser.RawConfigParser()
configFilePath=os.path.join(os.path.dirname(__file__), '..','config.ini')
config.read(configFilePath)
CampaignName=config.get('Lolagroove','Name')

def Lead_Scraper(df):       
    New_Data=[]
    for i in range(len(df)):
        try:
            row=df.iloc[i]
            print('processing ...', row['ID'])
            #fetch zoominfo url
            try:
                zoominfo_url=Search_Contact(row,'Zoominfo','Google') 
                # return first url from google search for zoominfo
                zoominfoData=Zoominfo_scraper(zoominfo_url,row['ID']) #Extract Revenue and Emp Size
                # Extract Linkedin URL Based on First Name , Last Name, Jobtitle and Company from LInkedin
            except:
                zoominfoData={}
                zoominfoData['company']=''
                zoominfoData['Revenue']=''
                zoominfoData['Employees']=''
                zoominfo_url=''
            try:
                linkedinurl=FetchLinkedinLink(row)
                linkedinurl=linkedinurl.split('?')[0]
                print('linkedin')
            except:
                linkedinurl=Search_Contact(row,'Linkedin','Google') # return first url from google search for Linkedin

            # get data from linkedin based on url scraped from Linkedin and Google Search
            try:
                LinkedinData=crawl(linkedinurl,row['ID'])
            except:
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
            except:
                DomainStatus=''
            try:
                addressEvidence=Main(row['Address 1'],row['Country'],row['Postal/Zip Code'],row['Company Name'],'Google',city=row['Town/City'])
            except:
                addressEvidence={'addressLink':'', 'accuracy':'', 'Text':'' }
            try:
                telephoneEvidence=PhoneValidation(row['Telephone'],row['Company Name'],'Google')
            except:
                telephoneEvidence=''

            if Zoominfo_company_match_status=='Company Name Not Matched' or Zoominfo_company_match_status=='Match Not Possible':
                zoominfoData['company']=''
                zoominfoData['Revenue']=''
                zoominfoData['Employees']=''
                zoominfo_url=''

            for i,industry in enumerate(LinkedIn_Industry):
                if industry.lower()==LinkedinData['LinkedinIndustry'].lower():
                    output_industry=lolagroove_Industry[i]
                    break
                else:
                    output_industry=''

            #update the scraped data to the existing file
            row['zoominfo_company']       = zoominfoData['company']  
            row['zoominfo_revenue']       = zoominfoData['Revenue']
            row['zoominfoEmployees']      = zoominfoData['Employees']
            row['linkedinfirstName']      = LinkedinData['firstName']
            row['linkedinlastName']       = LinkedinData['lastName']
            row['linkedinTitle']          = LinkedinData['Title']
            row['linkedinCompanyName']    = LinkedinData['CompanyName']
            row['linkedinCompanyEmpSize'] = LinkedinData['linkedinCompanyEmpSize']
            row['linkedinCompanyWebsite'] = LinkedinData['linkedinCompanyWebsite']
            row['LinkedinIndustry']       = output_industry
            row['Linkedin_company_match_status'] = company_match_status
            row['Zoominfo_company_match_status'] = Zoominfo_company_match_status
            row['LinkedinDomainStatus']   = DomainStatus
            row['addressMatchingScore']   = addressEvidence['accuracy']
            row['AddressText']            = addressEvidence['Text']
            dictData=row.to_dict()
            dictData['linkedin_id_url']   = LinkedinData['LinkedinContacturl']
            dictData['jobtitle_evidence'] = LinkedinData['LinkedinContacturl']
            dictData['company_evidence']  = LinkedinData['LinkedinCompanyURL']+'/about'
            dictData['companysize_evidence']  = LinkedinData['LinkedinCompanyURL']
            dictData['address_evidence']  = addressEvidence['addressLink']
            dictData['turnover_evidence'] = zoominfo_url
            dictData['phone_evidence']    = telephoneEvidence
            try:
                log_file_write(row['ID'],dictData)
            except:
                pass

            #append the scraped result to output list
            New_Data.append(dictData)  

        except:
            pass
        
    new_df=pd.DataFrame(New_Data)
    outputPath=os.path.join(os.getcwd(),'Processed Output')

    try:
        new_df.to_csv(outputPath+'/'+CampaignName+'.csv',encoding='utf-8')
    except:
        new_df.to_csv(outputPath+'/'+CampaignName+'.csv')
    print('Scraping Completed and output in Processed Output Folder')
