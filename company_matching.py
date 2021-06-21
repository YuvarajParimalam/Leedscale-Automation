
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unicodedata
from cleanco import cleanco
from tools.utiltity import Sanitiser

def required_company_name(expectNumber,sanitiseobject,regexFormat,givenData):
	try:
		if len(givenData)>= expectNumber:
			if sanitiseobject.regex_function(regexFormat, givenData) != []:
				requiredCompanyName = str(sanitiseobject.regex_function(regexFormat, givenData)[0])
				requiredCompanyName = requiredCompanyName.replace(' ', '')
			else:
				requiredCompanyName = str(givenData).replace(' ', '')
		else:
			requiredCompanyName = givenData
			
		return requiredCompanyName
		
	except Exception as s:
		raise s

def is_abbrev(abbrev, text):
	abbrev = abbrev.lower()
	text = text.lower()
	words = text.split()
	if not abbrev:
		return True
	if abbrev and not text:
		return False
	if abbrev[0]!=text[0]:
		return False
	else:
		return (is_abbrev(abbrev[1:],' '.join(words[1:])) or
				any(is_abbrev(abbrev[1:],text[i+1:])
					for i in range(len(words[0]))))			
def abbrevation_Check(CompanyOne,CompanyTwo):					
	try:
		CompanyOneCaseCheck = CompanyOne.isupper()
		CompanyTwoCaseCheck = CompanyTwo.isupper()
		
		if CompanyOneCaseCheck is True and CompanyTwoCaseCheck is False:
			CompanyTwoList = CompanyTwo.split(' ')
			CompanyTwoFirstLetters = [i[0] for i in CompanyTwoList]
			CompanyTwoAbbrevation = "" 
			for each in CompanyTwoFirstLetters: 
				CompanyTwoAbbrevation += each  
			if CompanyOne == CompanyTwoAbbrevation:
				companyMatchFlag = 'Special Partial Match - abbrevation match'
			else:
				
				companyMatchFlag = 'Company Name Not Matched'
		elif CompanyOneCaseCheck is False and CompanyTwoCaseCheck is True:
			CompanyOneList = CompanyOne.split(' ')
			CompanyOneFirstLetters = [i[0] for i in CompanyOneList]
			CompanyOneAbbrevation = "" 
			for each in CompanyOneFirstLetters: 
				CompanyOneAbbrevation += each  
			if CompanyTwo == CompanyOneAbbrevation:
				companyMatchFlag = 'Special Partial Match - abbrevation match'
			else:
				companyMatchFlag = 'Company Name Not Matched'
		else:
			companyMatchFlag = 'Company Name Not Matched'
		return companyMatchFlag
	except Exception as Company_Matching:
		
		return 'Company Name Not Matched'
		
def special_company_matching(inputCompany,outputCompany,searchMethod,inCompAbbr,outCompAbbr):
		inputCompany = inputCompany.lower().replace(' and ',' & ')
		outputCompany = outputCompany.lower().replace(' and ',' & ')
		inputCompany  = inputCompany.replace("("," ").replace(")"," ").replace("["," ").replace("]"," ").replace("."," ").replace("+"," ").replace("-"," ").replace(","," ").replace(","," ")
		outputCompany  = outputCompany.replace("("," ").replace(")"," ").replace("["," ").replace("]"," ").replace("."," ").replace("+"," ").replace("-"," ").replace(","," ").replace(","," ")
		
		inputCompanySplit = list(filter(None, inputCompany.split(" ")))
		outputCompanySplit = list(filter(None, outputCompany.split(" ")))

		directWordMatchCount = 0
		partialWordMatchCountIPOP = 0
		partialWordMatchCountOPIP = 0
		
		directWordMatchCountUpdated = 0
		partialWordMatchCountIPOPUpdated = 0
		partialWordMatchCountOPIPUpdated = 0
		
		companyMatchFlag = 'Company Name Not Matched'
		matchedwordlist = []
		matchedwordlistinput = []
		matchedwordlistoutput = []

		# step 1 : Matching words in the input directly with the output list
			
		# input to output lookup
		for word in inputCompanySplit:
			data = word
			if word in outputCompanySplit and len(word)>1:
				directWordMatchCount = directWordMatchCount + 1
				matchedwordlist.append(word)
			
			# step 2 : Matching words in the input using "starts with" logic with the output list	
			if word.startswith(tuple(outputCompanySplit)):
				
				partialWordMatchCountOPIP = partialWordMatchCountOPIP + 1
				matchedwordlistinput.append(data)
					
		# output to input lookup		
		for word in outputCompanySplit:
			data = word
			
			# step 2 : Matching words in the output using "starts with" logic with the input list
			if word.startswith(tuple(inputCompanySplit)):
				partialWordMatchCountIPOP = partialWordMatchCountIPOP + 1
				matchedwordlistoutput.append(data)
		
		if directWordMatchCount >=1:
			companyMatchFlag = 'Special Partial Match - Complete words('+str(directWordMatchCount)+') | '+str(matchedwordlist)
		
		elif partialWordMatchCountIPOP >=1:
			companyMatchFlag = 'Special Partial Match - IP words startswith OP words('+str(partialWordMatchCountIPOP)+') | '+str(matchedwordlistoutput)
		
		elif partialWordMatchCountOPIP >=1:
			companyMatchFlag = 'Special Partial Match - OP words startswith IP words('+str(partialWordMatchCountOPIP)+') | '+str(matchedwordlistinput)
		
		elif is_abbrev(inputCompany, outputCompany) or is_abbrev(outputCompany, inputCompany):
			companyMatchFlag = 'Special Partial Match - abbrevation match'
			
		if 	companyMatchFlag == 'Company Name Not Matched':
			
			companyMatchFlag = abbrevation_Check(inCompAbbr,outCompAbbr)
		return companyMatchFlag	
			
def comparision(inputCompany,outputCompany,inputCompanyCleaned,outputCompanyCleaned,inputCompanyFirst15,inputCompanyLast15,outputCompanyLast15,outputCompanyFirst15,outputCompanyFirst12,inputCompanyFirst12,outputCompanyLast12,inputCompanyLast12,inputCompanyFirst2words,outputCompanyFirst2words,searchMethod):
	
	companyFlag =''
	if outputCompany.lower().strip() == inputCompany.lower().strip():
		companyFlag = 'Exact Match'
	elif inputCompanyCleaned.lower().strip() == outputCompanyCleaned.lower().strip():
		companyFlag = 'Exact Match'
	elif inputCompany.lower().strip() in outputCompany.lower().strip():
		companyFlag = 'Input Name Full Match Without Spl Char'
	elif outputCompany.lower().strip() in inputCompany.lower().strip():
		companyFlag = 'Output Name Full Match Without Spl Char'
	elif outputCompanyFirst15.lower().strip() in inputCompany.lower().replace(' ', '').strip():
		companyFlag = 'Output First 15 Char Match'
	elif inputCompanyFirst15.lower().strip() in outputCompany.lower().replace(' ', '').strip():
		companyFlag = 'Input First 15 Char Match'
	elif outputCompanyLast15.lower().strip() in inputCompany.lower().replace(' ', '').strip():
		companyFlag = 'Output Last 15 Char Match'
	elif inputCompanyLast15.lower().strip() in outputCompany.lower().replace(' ', '').strip():
		companyFlag = 'Input Last 15 Char Match'
	
	elif unicodedata.normalize('NFKD', inputCompany.strip()).encode('ascii', 'ignore') == unicodedata.normalize('NFKD',outputCompany.strip()).encode('ascii', 'ignore'):
		companyFlag = 'Exact Match'
	elif unicodedata.normalize('NFKD', inputCompanyCleaned.strip()).encode('ascii','ignore') == unicodedata.normalize('NFKD',outputCompanyCleaned.strip()).encode('ascii', 'ignore'):
		companyFlag = 'Exact Match'
	elif unicodedata.normalize('NFKD', inputCompany.strip()).encode('ascii', 'ignore') in unicodedata.normalize('NFKD',outputCompany.strip()).encode('ascii', 'ignore'):
		companyFlag = 'Input Name Full Match Without Spl Char'
	elif unicodedata.normalize('NFKD', outputCompany.strip()).encode('ascii', 'ignore') in unicodedata.normalize('NFKD', inputCompany.strip()).encode('ascii', 'ignore'):
		companyFlag = 'Output Name Full Match Without Spl Char'
	elif unicodedata.normalize('NFKD', outputCompanyFirst15.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD', inputCompany.strip().replace(' ', '')).encode('ascii', 'ignore'):
		companyFlag = 'Output First 15 Char Match'
	elif unicodedata.normalize('NFKD', inputCompanyFirst15.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD',outputCompany.strip().replace(' ','')).encode('ascii', 'ignore'):
		companyFlag = 'Input First 15 Char Match'
	elif unicodedata.normalize('NFKD', outputCompanyFirst15.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD',inputCompany.strip().replace(' ','')).encode('ascii', 'ignore'):
		companyFlag = 'Output Last 15 Char Match'
	elif unicodedata.normalize('NFKD', inputCompanyLast15.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD',outputCompany.strip().replace(' ','')).encode('ascii', 'ignore'):
		companyFlag = 'Input Last 15 Char Match'
	
	else:
		if searchMethod == 'Contact Verification':
			if outputCompanyFirst12.lower().strip() in inputCompany.lower().replace(' ', '').strip():
				companyFlag = 'Output First 12 Char Match'
			elif inputCompanyFirst12.lower().strip() in outputCompany.lower().replace(' ', '').strip():
				companyFlag = 'Input First 12 Char Match'
			elif outputCompanyLast12.lower().strip() in inputCompany.lower().replace(' ', '').strip():
				companyFlag = 'Output Last 12 Char Match'
			elif inputCompanyLast12.lower().strip() in outputCompany.lower().replace(' ', '').strip():
				print("im in")
				companyFlag = 'Input Last 12 Char Match'
			elif unicodedata.normalize('NFKD', outputCompanyFirst12.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD', inputCompany.strip().replace(' ', '')).encode('ascii', 'ignore'):
				companyFlag = 'Output First 12 Char Match'
			elif unicodedata.normalize('NFKD', inputCompanyFirst12.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD', outputCompany.strip().replace(' ', '')).encode('ascii', 'ignore'):
				companyFlag = 'Input First 12 Char Match'
			elif unicodedata.normalize('NFKD', outputCompanyLast12.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD', inputCompany.strip().replace(' ', '')).encode('ascii', 'ignore'):
				companyFlag = 'Output Last 12 Char Match'
			elif unicodedata.normalize('NFKD', inputCompanyLast12.strip()).encode('ascii','ignore') in unicodedata.normalize('NFKD', outputCompany.strip().replace(' ', '')).encode('ascii', 'ignore'):
				companyFlag = 'Input Last 12 Char Match'
			else:
				companyFlag = 'Company Name Not Matched'
		else:
			companyFlag = 'Company Name Not Matched'	
		
	return companyFlag
	
def match_company_name(inputCompany ,outputCompany ,searchMethod= None):

	"""Function to Match 'inputCompany' and 'outputCompany' to return the Company matching status."""
	try:
		# suspicious block of code
		sanitiseobject = Sanitiser()
		inCompAbbr = inputCompany.replace(' and ', ' & ').replace(' & ','&')
		outCompAbbr = outputCompany.replace(' and ', ' & ').replace(' & ','&')
		inputCompany = inputCompany.lower().replace(' and ', ' & ').replace(' & ','&')
		outputCompany = outputCompany.lower().replace(' and ', ' & ').replace(' & ','&')

		if len(inputCompany ) >=5:
			inputCompany  = cleanco(inputCompany.replace('. ' ,'.')).clean_name()
			inputCompanyCleaned = ''.join(e for e in inputCompany if e.isalnum())
		else:
			inputCompanyCleaned = ''.join(e for e in inputCompany if e.isalnum())
			
		if len(outputCompany ) >=5:
			outputCompany = cleanco(outputCompany.replace('. ' ,'.')).clean_name()
			outputCompanyCleaned = ''.join(e for e in outputCompany if e.isalnum())
		else:
			outputCompanyCleaned = ''.join(e for e in outputCompany if e.isalnum())
	
		inputCompanyFirst15 = required_company_name(15, sanitiseobject, 'companyFirst15',inputCompany)
		inputCompanyLast15 = required_company_name(15, sanitiseobject, 'companyLast15',inputCompany)
		outputCompanyFirst15 = required_company_name(15, sanitiseobject, 'companyFirst15',outputCompany)
		outputCompanyLast15 = required_company_name(15, sanitiseobject, 'companyLast15',outputCompany)

		inputCompanyFirst12 = required_company_name(12, sanitiseobject, 'companyFirst12',inputCompany)
		inputCompanyLast12 = required_company_name(12, sanitiseobject, 'companyLast12',inputCompany)
		outputCompanyFirst12 = required_company_name(12, sanitiseobject, 'companyFirst12',outputCompany)
		outputCompanyLast12 = required_company_name(12, sanitiseobject, 'companyLast12',outputCompany)

		inputCompanyFirst2words = required_company_name(12, sanitiseobject, 'companyFirst2',inputCompany)
		outputCompanyFirst2words = required_company_name(12, sanitiseobject, 'companyFirst2',outputCompany)
		
		if len(inputCompanyFirst2words) < 5:
			inputCompanyFirst2words = ''
		if len(outputCompanyFirst2words) < 5:
			outputCompanyFirst2words = ''

		if len(inputCompany ) <1 or len(outputCompany ) <1 :
			companyFlag = 'Match Not Possible'
		else:
			companyFlag = comparision(inputCompany,outputCompany,inputCompanyCleaned,outputCompanyCleaned,inputCompanyFirst15,inputCompanyLast15,outputCompanyLast15,outputCompanyFirst15,outputCompanyFirst12,inputCompanyFirst12,outputCompanyLast12,inputCompanyLast12,inputCompanyFirst2words,outputCompanyFirst2words,searchMethod)

		if companyFlag == 'Company Name Not Matched':
				companyFlag = special_company_matching(inputCompany,outputCompany,searchMethod,inCompAbbr,outCompAbbr)
				
		if companyFlag == 'Company Name Not Matched':
			inputCompanyFirstLetter = inputCompany[0]
			outputCompanyFirstLetter = outputCompany[0]
			
			if inputCompanyFirstLetter == outputCompanyFirstLetter:
				companyFlag = 'Company Name Not Matched - First Letter Match' 
			else:
				companyFlag = 'Company Name Not Matched'
		return companyFlag

	except Exception as Company_Matching:
		print('error',Company_Matching)

