import configparser, os
from Scripts.Lolagroove import Lolagroove
from Scripts.Lead_Processor import Lead_Scraper
from Scripts.Campaign_update import Lead_Update


config = configparser.RawConfigParser()
configFilePath=os.path.join(os.getcwd(),'config.ini')
config.read(configFilePath)
CampaignName=config.get('Lolagroove','Name')
filename=config.get('fileupload','filename')
URL=config.get('Lolagroove','URL')
uploadFilePath=os.path.join(os.getcwd(),'Upload Files')
uploadFileName=os.path.join(uploadFilePath,filename)
detail=config.get('input','detail')

if __name__=='__main__':

    if detail=='download' :   
        #Downloading file
        df=Lolagroove(CampaignName)
        #Processing file
        output=Lead_Scraper(df)
    else:
        #uploading File
        file_upload=Lead_Update(URL,uploadFileName)
