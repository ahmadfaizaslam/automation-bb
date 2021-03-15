import pandas as pd
import os
import logging
from my_files import*
from my_functions import*


print('1. Loading Files...\n')
master = file.master

print('Master file loaded completed.')
print(master.shape)
print()

class comparison:
    
    def __init__(self,file_name,sheet,check1,df,e):
        self.file_name = file_name
        self.sheet = sheet
        self.check1 = check1
        self.df = df
        self.e =e
        
    frames ={}
    
    for file_name,sheet in file.validation.items(): 
        frames[file_name] = load_files(file_name,sheet)
        print(f"2. Checking Master file against {file_name}")
        try:
            df=master.merge(frames[file_name],how='left',left_on='Account_Num',right_on='Account_No')
            print()
        except Exception as e:
            print(f"    File {file_name} is not compatible \n   !! {e} is not found \n")
            print('___________________________')
            continue
        
        check1=df[df['Account_No'].notnull()][['Account_Num','Balance','M_Bnm_Balance_SUM1']]
        if check1[check1['Balance']!=check1['M_Bnm_Balance_SUM1']].shape[0]==0:
            print("    ODTL numbers are all matched.\n")
            print('___________________________')

        else:
            print("Not matched; Check Unmatched Balance ODTL excel file")
            print('___________________________')

