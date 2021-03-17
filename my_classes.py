import pandas as pd
from my_files import*
import os
path = os.path.dirname(os.path.realpath(__file__))

class my_comparison:
    def __init__(self,filename,sheet):
        self.filename = filename
        self.sheet = sheet
        self.file_path = path+"\\MIS\\"+filename+".xlsx"
        self.dataframe = pd.read_excel(self.file_path,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object})
        self.shape = self.dataframe.shape
        
    def comparison(self,master,column_1,column_2):
        print(f"        {self.shape}")
        df=master.merge(self.dataframe,how='inner',left_on=column_1,right_on=column_2)
        return df
    
    def odtl_check(self,column_1,column_2):
        if self[self[column_1]!=self[column_2]].shape[0]==0:
            print("        ODTL numbers are all matched.")
        else:
            print("        Not matched; Check Unmatched Balance ODTL excel file")