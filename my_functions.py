import pandas as pd
from my_files import*



def load_files(file_name,sheet):
    excel_file = file.dir_path +"\MIS\\"+file_name+".xlsx"
    df=pd.read_excel(excel_file,sheet_name=sheet,dtype={'Account_No':str,'M_Cus_No':object})
    print(f"1. File {file_name} is loaded")
    print("    Dimension :",df.shape)
    return df
