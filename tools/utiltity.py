
import os
import sys
import json
import re
import time
from urllib. parse import urlparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def file_cleanup():

    '''Function to clean up the expired cookie file'''
    try:
        now = time.time()
        directories = ['cookie']

        for directory in directories:
            path = os.path.join(os.getcwd(), directory)
            if os.path.isdir(path) == True:
                for filename in os.listdir(path):
                    if os.path.getmtime(os.path.join(path, filename)) < now - 1 * 86400:
                        if os.path.isfile(os.path.join(path, filename)):
                            print("Removing Files : "+ filename)
                            os.remove(os.path.join(path, filename))

    except Exception as fileCleanupExp:
        print(fileCleanupExp,'File Clean Up Exception')

def CheckDomain(email,website):
    emaildomain=email.split('@')[1]
    website=urlparse(website).netloc.replace('www.','')
    if emaildomain==website:
        return 'Exact Match'
    elif emaildomain in website:
        return 'Email in Website'
    else:
        return 'No Match'
        
    		

class Sanitiser:
	
	def __init__(self):
	
		self.jsonData = json.load(open('tools/databot_pattern_matching.json', encoding='utf-8'))
		
	def regex_function(self,regexstring,pageContent):

		regex = self.jsonData.get(regexstring)[1]
		regexEntity = re.findall(regex,pageContent,re.I)
		return regexEntity
	
	def soup_function(self, soupstring):
	   
		if self.jsonData.get(soupstring)[0]=='Soup':
			soupEntity = self.jsonData.get(soupstring)[1].split(',')
			soupTag = str(eval(soupEntity[0].strip()))
			soupAttribute = eval(soupEntity[1].strip())
		
		else:
			print("No soup element found!")
			soupTag,soupAttribute ='',''
			
		return soupTag,soupAttribute
		
	def __del__(self):
		pass