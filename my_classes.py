import pandas as pd
from my_files import*
import os
path = os.path.dirname(os.path.realpath(__file__))

class my_validation:
    def __init__(self, filename,sheet,merge_on,check_on):
        self.filename = filename,
        self.sheet = sheet,
        self.merge_on = merge_on
        self.check_on = check_on
        self.file_path = path+"\\MIS\\"+filename+".xlsx"                 #for mis
        self.dataframe= pd.read_excel(self.file_path,sheet_name=sheet,
                        dtype={merge_on:str,check_on:int}).rename(
                        columns={
                        merge_on: "Account_No",
                        check_on: 'M_Bnm_Balance' 
                        }).fillna(0)
        self.shape = self.dataframe.shape
        
    def comparison(self,master,column_1,column_2):
        print(f"        Dimension : {self.shape}")
        df=master.merge(self.dataframe,how='inner',left_on=column_1,right_on=column_2)
        return df
                       
    def odtl_check(self,column_1,column_2):
        if self[self[column_1]!=self[column_2]].shape[0]==0:
            print("        ODTL numbers are all matched.")
        else:
            print("        Not matched; Check Unmatched Balance ODTL excel file")
            
    def tagging(self,sheet,merge_on,check_on,skiprow):
        file_path = path+"\\Code and reference\\"+self+".xlsx"   #for code and reference
        dataframe = pd.read_excel(file_path,
                                       sheet_name=sheet,
                                       skiprows=skiprow,
                                       dtype={merge_on:str,check_on:str})
        print(dataframe.shape)
    def ccnt(self,column_1,column_2,column_3):
        concatenation = self.dataframe[[column_1,column_2,column_3]].copy()
        return concatenation


class my_transformation:
    def __init__(self, filename,sheet,merge_on,check_on,skiprow):
        self.filename = filename,
        self.sheet = sheet,
        self.merge_on = merge_on
        self.check_on = check_on
        self.file_path = path+"\\\Code and reference\\"+filename+".xlsx"                 #for mis
        self.dataframe= pd.read_excel(
                        self.file_path,
                        sheet_name=sheet,
                        skiprows=skiprow,
                        dtype={merge_on:str,check_on:int})
        self.shape = self.dataframe.shape

    def taggging(self):
        print(self.filename)