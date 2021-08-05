# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import logging
import shutil
from datetime import datetime
import time

def log_cleanup_dir(linkID = None):
		
		'''Function to clean up the expired log files and folders'''
		linkID = '0000' if linkID is None else linkID
		try:
			now = time.time()
			directories = [d for d in os.listdir('LogFolder') if os.path.isdir(os.path.join('LogFolder', d))]
			
			for directory in directories:
				path = os.path.join(os.getcwd(),"LogFolder", directory)
				
				if os.path.isdir(path) == True:
					
					if os.path.getmtime(os.path.join(path)) < now - 2 * 86400:
						print("Removing Files : "+ directory)
						shutil.rmtree(path)
					
		except Exception as fileCleanupExp:
			print(fileCleanupExp)
	
def create_log_fileName(id):
	'''createLogFileName function is create the log file name '''
	logFileDir="LogFolder"
	logFileName=str(id)+'_'
	if not os.path.exists(logFileDir):
		os.makedirs(logFileDir)
	logFileDir=str(logFileDir)+"/"+str(datetime.strftime(datetime.now(),"%d%m%Y"))
	if not os.path.exists(logFileDir):
		os.makedirs(logFileDir)	
	logFile=logFileDir+"/"+str(logFileName)+str(datetime.strftime(datetime.now(),"%Y%m%d_%H"))+".log"
	return logFile
	
def log_file_write(id,logtime):
	'''This function get the Log file from create_log_fileName function and write the Log file '''
	logFile=create_log_fileName(id)
	logging.basicConfig(filename=logFile,level=logging.INFO) 
	logging.info(str(datetime.strftime(datetime.now(),"%d-%m-%Y:%H:%M:%S")+"|""|"+str(id)+"|"+str(logtime)))
	
