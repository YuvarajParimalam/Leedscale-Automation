import pandas as pd
df=pd.read_csv('Processed Output\Sitecore_Americas_PPL_Q1_FY22 4 (Allchecks).csv')
countrylist=list(df['Country'])
df2=pd.read_excel('Country_Codes.xlsx')
country=list(df2['Country'])
code=list(df2['Code'])
countrycode=[]
for inputcountry in countrylist: 
    for i in range(len(country)):
        if inputcountry.lower()==country[i].lower():
            countrycode.append(code[i])
            break
phone=list(df['Telephone'])
countrycode=countrycode
print(phone)
print(countrycode)