import pandas as pd
df=pd.read_csv('Scandit_EMEA_R_P_FY21_Q2 4 (Allchecks).csv')
countrycode=list(df['CountryCode'])
phone=list(df['Telephone'])
print(phone)
print(countrycode)