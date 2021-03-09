import pandas as pd
import os
import logging
#read txt file that is in the same directory



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
print('Master file loaded completed.')
print()


def load_files(files):
    for file_name,sheet in files.items():
        # frames.append(pd.read_excel(excel_file,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object}))
        excel_file = dir_path + "\MIS\\"+file_name
        df=pd.read_excel(excel_file,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object})
        frames[file_name] = df
        print(f"File {file_name} is loaded")
    print()
    
    
    
def check1(frames):
    for file,frame in frames.items():
        print(f"Checking Master file against {file}")
        try:
            df=master_file.merge(frame,how='left',left_on='Account_Num',right_on='Account_No')
        except Exception as e:
            print(f"File {file_name} is not compatible")
            print (str(e) , "is not found")
            break
            
        check1=df[df['Account_No'].notnull()][['Account_Num','Balance','M_Bnm_Balance_SUM1']]
        if check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']].shape[0]==0:
            print('ODTL numbers are all matched.')

        else:
            df_unmatched=check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']]
            df_unmatched.to_excel(dir_path+"Unmatched Balance ODTL.xlsx",engine='openpyxl')
            print('Not matched; Check Unmatched Balance ODTL excel file')

    print("==================================================================")
    
    
if __name__ == "__main__":
    load_files(files)
    check1(frames)

