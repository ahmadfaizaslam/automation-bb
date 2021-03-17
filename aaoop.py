import pandas as pd
import os
import logging
from my_functions import*
import json

path = os.path.dirname(os.path.realpath(__file__))
with open('my_files.json') as json_file: 
    files = json.load(json_file)
    
master =  pd.read_csv(path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',
                           parse_dates=['NPL_Date','RISK_RATG_DT'],
                           dtype={'Party_Id':object,'SPL_MENTION_ACCT_IND':object})
print('Master file loaded completed.')
# print(files['comparison'][0]['filename']) accessing file
  
class my_comparison:
    def __init__(self,filename,sheet,extension):
        self.filename = filename
        self.sheet = sheet
        self.extension = extension
        self.file_path = path+"\\MIS\\"+filename+extension
        self.dataframe = pd.read_excel(self.file_path,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object})
    
      
for i in files['comparison']:
    x = (i['filename']).replace(" ","")
    x = my_comparison((i['filename']),(i['sheet']),(i['extension']))
    print("1. File "+ (i['filename'])+" is loaded")
    print("    Dimension :",x.dataframe.shape)
    print("2. Checking Master file against", (i['filename']))
    try:
        df=master.merge(x.dataframe,how='left',left_on='Account_Num',right_on='Account_No')
    except Exception as e:
            print(f"    File x.dataframe is not compatible \n   !! {e} is not found \n")
            print('___________________________')
            continue
    check1=df[df['Account_No'].notnull()][['Account_Num','Balance','M_Bnm_Balance_SUM1']]
    if check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']].shape[0]==0:
        print("    ODTL numbers are all matched.\n")
        print('___________________________')

    else:
        print("Not matched; Check Unmatched Balance ODTL excel file")
        print('___________________________')
    # Data1 = my_comparison("xx","xxx","xxs")

