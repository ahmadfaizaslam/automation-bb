import pandas as pd
import os
import logging
 
dir_path = os.path.dirname(os.path.realpath(__file__))
x = open("files.txt", "r")
files = {}
frames = {}

for line in x:
        pos = line.find(':')
        file_name = line[:pos]
        sheet_name = line[pos:].rstrip("\n").replace(":","").replace(" ","")
        files[file_name] = sheet_name

print('1. Loading Files...\n')
master_file =  pd.read_csv(dir_path + r"\bb.txt",
                        delimiter = "\t",
                        header =0,
                        na_values='?',
                        engine='python',
                        parse_dates=['NPL_Date','RISK_RATG_DT'],
                        dtype={'Party_Id':object,'SPL_MENTION_ACCT_IND':object})
print('Master file loaded.')
print()
    

class mis_v_redw():

    def load_files(self):
        for file_name,sheet in files.items():
            excel_file = dir_path + "\MIS\\"+file_name
            df=pd.read_excel(excel_file,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object})
            frames[file_name] = df
            shape = frames[file_name].shape
            print(f"File {file_name} is loaded \nDimension :{shape} \n" )
        
        print("==== All Secondary files are loaded. ")
        print()

        
    def odtl_check(self):
        for file,frame in frames.items():
            print(f"Checking Master file against {file}")
            try:
                df=master_file.merge(frame,how='left',left_on='Account_Num',right_on='Account_No')
            except Exception as e:
                print(f"File {file_name} is not compatible \n !! {e} is not found \n")
                continue
                
            check1=df[df['Account_No'].notnull()][['Account_Num','Balance','M_Bnm_Balance_SUM1']]
            if check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']].shape[0]==0:
                print("    ODTL numbers are all matched.\n")

            else:
                df_unmatched=check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']]
                df_unmatched.to_excel(dir_path+"Unmatched Balance ODTL.xlsx",engine='openpyxl')
                print('Not matched; Check Unmatched Balance ODTL excel file')

        print("====END====")

