import configparser, os
from Scripts.Lolagroove import Lolagroove
from Scripts.Lead_Processor import Lead_Scraper
from Scripts.Campaign_update import Lead_Update


config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
CampaignName=config.get('Lolagroove','Name')
filename=config.get('fileupload','filename')
uploadFilePath=os.path.join(os.getcwd(),'Upload Files')
uploadFileName=os.path.join(uploadFilePath,filename)


if __name__=='__main__':
        
    #Downloading file
    df=Lolagroove(CampaignName)

    #Processing file
    output=Lead_Scraper(df)

    #uploading File
    file_upload=Lead_Update(uploadFileName)
