from my_files import*
import itertools
path = os.path.dirname(os.path.realpath(__file__))
master =  file.master
bullet = 1
pd.set_option('display.max_rows', None) 
class testter:

    def __init__(self, filename,sheet,merge_on,check_on):
        self.filename = filename,
        self.sheet = sheet,
        self.merge_on = merge_on
        self.check_on = check_on
        self.file_path = path+"\\MIS\\"+filename+".xlsx"
        self.dataframe = pd.read_excel(self.file_path,sheet_name=sheet,
                         dtype={merge_on:str,check_on:int}).rename(
                             columns={
                                merge_on: "Account_No",
                                check_on: 'M_Bnm_Balance' 
                             })
        self.shape = self.dataframe.shape
    
    def comparison(self,master,column_1,column_2):
        print(f"        Dimension : {self.shape}")
        df=master.merge(self.dataframe,how='inner',left_on=column_1,right_on=column_2)
        return df
    
    def odtl_check(self,column_1,column_2):
        if self[self[column_1]!=self[column_2]].shape[0]==0:
            # print("        ODTL numbers are all matched.")
            print("noice")
        else:
            print("not noice")
            print(self.shape)
    
    
for x,y in file.validation.items():
    files = file.validation[x]
    classname = testter(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
    print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
    try:    
        merged = testter.comparison(classname,master,"Account_Num","Account_No")
        testter.odtl_check(merged,'Balance','M_Bnm_Balance')
    except Exception as e:
        print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
        pass
    bullet = bullet + 1