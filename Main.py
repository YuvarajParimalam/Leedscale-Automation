
import pandas as pd
import os
from urllib.parse import quote
pd.options.mode.chained_assignment = None

from Scripts.Google_Search import Search_Contact
from Scripts.Linkedin import crawl,FetchLinkedinLink
from tools.utiltity import file_cleanup,CheckDomain
from Scripts.Zoominfo import Zoominfo_scraper
from Scripts.company_matching import match_company_name
from Scripts.Lolagroove import Lolagroove
from Scripts.AddressEvidence import Main
import sys
from Scripts.PhoneEvidence import PhoneValidation

input=sys.argv[1]
df=Lolagroove(input)

# file_cleanup()
'''
outputPath=os.path.join(os.getcwd(),'Output')
df=pd.read_csv(os.path.join(outputPath,'Adobe_Digital_Foundation_Q1_FY21 4 (Allchecks).csv'))
New_Data=[]
for i in range(len(df)):
    try:
        row=df.iloc[i]
        #fetch zoominfo url
        zoominfo_url=Search_Contact(row,'Zoominfo','bing') 
        # return first url from google search for zoominfo
        zoominfoData=Zoominfo_scraper(zoominfo_url,row['ID']) #Extract Revenue and Emp Size
        # Extract Linkedin URL Based on First Name , Last Name, Jobtitle and Company from LInkedin
        try:
            linkedinurl=FetchLinkedinLink(row)
            linkedinurl=linkedinurl.split('?')[0]
        except:
            linkedinurl=Search_Contact(row,'Linkedin','bing') # return first url from google search for Linkedin

        # get data from linkedin based on url scraped from Linkedin and Google Search
        if 'linkedin.com/' in linkedinurl:
            LinkedinData=crawl(linkedinurl,row['ID'])
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
        except:
            DomainStatus=''
        try:
            addressEvidence=Main(row['Address 1'],row['Country'],row['Postal/Zip Code'],row['Company Name'],'Bing',city=row['Town/City'])
        except:
            addressEvidence={'addressLink':'', 'accuracy':'', 'Text':'' }
        try:
            telephoneEvidence=PhoneValidation(row['Telephone'],row['Company Name'],'Bing')
        except:
            telephoneEvidence=''

        if Zoominfo_company_match_status=='Company Name Not Matched' or Zoominfo_company_match_status=='Match Not Possible':
            zoominfoData['company']=''
            zoominfoData['Revenue']=''
            zoominfoData['Employees']=''
            zoominfo_url=''

        #update the scraped data to the existing file
        row['zoominfo_company']  = zoominfoData['company']  
        row['zoominfo_revenue']  = zoominfoData['Revenue']
        row['zoominfoEmployees'] = zoominfoData['Employees']
        row['zoominfo_url']      = zoominfo_url
        row['linkedinfirstName'] = LinkedinData['firstName']
        row['linkedinlastName']  = LinkedinData['lastName']
        row['linkedinTitle']     = LinkedinData['Title']
        row['linkedinCompanyName'] = LinkedinData['CompanyName']
        row['LinkedinContacturl']  = LinkedinData['LinkedinContacturl']
        row['LinkedinCompanyURL']  = LinkedinData['LinkedinCompanyURL']
        row['linkedinCompanyEmpSize'] = LinkedinData['linkedinCompanyEmpSize']
        row['linkedinCompanyWebsite'] = LinkedinData['linkedinCompanyWebsite']
        row['Linkedin_company_match_status'] = company_match_status
        row['Zoominfo_company_match_status'] = Zoominfo_company_match_status
        row['LinkedinDomainStatus'] = DomainStatus
        row['AddressLink'] = addressEvidence['addressLink']
        row['addressMatchingScore'] = addressEvidence['accuracy']
        row['AddressText'] = addressEvidence['Text']
        row['telephoneEvidence'] = telephoneEvidence
        #append the scraped result to output list
        New_Data.append(row.to_dict())
    except:
        pass
new_df=pd.DataFrame(New_Data)
new_df.to_csv('Final_Data_new.csv')
'''