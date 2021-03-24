import pandas as pd
import os
from my_classes import*
from my_files import*

bullet = 1
master =  file.master
print('\n Master file loaded. \n')
mis_dfs = []

if __name__ == "__main__":
    #for validating MIS with the bb.txt file
    for classname,elements in file.validation.items():
        files = file.validation[classname]
        classname = my_validation(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:    
            merged = my_validation.comparison(classname,master,"Account_Num","Account_No")
            dfs = my_validation.odtl_check(merged,'Balance','M_Bnm_Balance')
            mis_dfs.append(dfs)
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1
    print("================================")         
    mis_dfs = pd.concat(mis_dfs)
    mis_dfs = mis_dfs[['M_Cus_No','BC_NAME','REGION']].astype(str) #this will merge to masterbb1
    


print(mis_dfs.info())