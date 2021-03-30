import pandas as pd
from my_files import*
import os
import numpy as np
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
                        merge_on: 'Account_No',
                        check_on: 'M_Bnm_Balance'
                        }).fillna(0)
        self.shape = self.dataframe.shape

    def series(self):
        df = self.dataframe
        return df

    def comparison(self,master,column_1,column_2):
        print(f"        Dimension : {self.shape}")
        df=master.merge(self.dataframe,how='inner',left_on=column_1,right_on=column_2)
        return df

    def odtl_check(self,column_1,column_2):
        if self[self[column_1]!=self[column_2]].shape[0]==0:
            print("        ODTL numbers are all matched.")
            return self
        else:
            print("        Not matched; Check Unmatched Balance ODTL excel file")
            print("        Balance and M_Bnm_Balance are not matched")
            self.to_excel(path+r"\\log_file.xlsx",engine='openpyxl',index=False)
            print("        Error Has Been Saved in log_fil.xlsx")
            return self

class my_transformation:
    def __init__(self, filename,sheet,merge_on,check_on,skiprow):
        self.filename = filename,
        self.sheet = sheet,
        self.merge_on = merge_on
        self.check_on = check_on
        self.skiprow = skiprow
        self.file_path = path+"\\\Code and reference\\"+filename+".xlsx"    #for mis
        self.dataframe= pd.read_excel(
                        self.file_path,
                        sheet_name=sheet,
                        skiprows=skiprow,
                        dtype={merge_on:str,check_on:str})
        self.shape = self.dataframe.shape

    def tag(self,old_column,new_column,my_dictionary):
        df=self
        df[new_column]=""
        for condition,value in my_dictionary.items():
            df[new_column].mask(df[old_column]==condition, value,inplace=True)

        # df.to_excel(path+r"\\test.xlsx",engine='openpyxl')
        # print(df.info())
        return df

    def create_column(self,new_column_name,column_value):
        df = self.dataframe
        df[new_column_name] = column_value
        return df

    def colummn_create(df,new_column_name,column_value):
        df[new_column_name] = column_value
        return df

    def calculation(self,new_column,column_1,column_2):
        df = self.dataframe
        df[new_column]=(np.floor(pd.to_numeric(df[column_2])/1000))*1000
        df = df[[column_2,column_1,new_column]].rename(columns={column_2: 'NOB'}).dropna()
        df[new_column] = df[new_column].round().astype(float).astype(int).astype(str)
        return  df

    def get_gil(self,*columns):
        columns = list(columns)
        df = self
        df = df[columns]
        return df

    def get_nob(self,column_1,column_2,column_3):
        df = self
        df = self.dataframe
        df[column_1] =df[column_1].astype(str).str.strip()
        df=df[[column_1,column_2,column_3]]
        return df

    def do_merge(df_a,df_b,left_column,right_colunm):
        df_a = df_a.merge(df_b,how='left',left_on=left_column,right_on=right_colunm)
        return df_a

    def copy_value(df,value_from,value_to):
        # df[value_to].mask(df[value_to].isnull(), df[value_from], inplace=True)
        df[value_to].fillna(df[value_from], inplace=True)
        # df.loc[df[value_to].isna(), value_to] = df[value_from]
    #   masterbb2.loc[masterbb2['BC_NAME_y'].isnull(), 'BC_NAME_y'] = masterbb2['BC_NAME_x']
        return df

    def conditional_copy(df,value_from,value_to,cond,effect):
        df.loc[df[value_from] == cond, value_to] = effect
        return df

    def sconditional_copy(df,value_from,value_to,effect):
        df.loc[value_from, value_to] = effect
        return df

   