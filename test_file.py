import pandas as pd
from my_files import*
import os
import itertools
master =  file.master
path = os.path.dirname(os.path.realpath(__file__))


class my_automation:
    def __init__(self,filename,sheet):
        self.filename = filename
        self.sheet = sheet
        self.file_path = path+"\\MIS\\"+filename+".xlsx"
        self.dataframe = pd.read_excel(self.file_path,sheet_name=sheet,
                            dtype={"Account_No":str,"M_Account_No":str}).rename(columns={
                            "M_Account_No" : "Account_No"})
        self.shape = self.dataframe.shape
        
    def testtest(self):
        print(self.filename)
        print(self.dataframe.info())
    
    def comparison(self,master,column_1,column_2):
        print(self.filename)
        print(f"        Dimension : {self.shape}")
        df=master.merge(self.dataframe,how='left',left_on=column_1,right_on=column_2)
        print(df.shape)
        return df
       
for filename, sheet in ( 
        itertools.chain.from_iterable( 
            [itertools.product((filename, ), sheet) for filename, sheet in file.validation.items()])): 
                print()
                classname = filename.replace(" ","")
                classname = my_automation(filename,sheet)
                #my_automation.testtest(classname)
                try:
                    merged = my_automation.comparison(classname,master,"Account_Num","Account_No")
                    
                    print("ok")
                except:
                    print("not ok")
                    