import pandas as pd
import os
from my_classes import*
from my_files import*

bullet = 1
master =  file.master
print('\n Master file loaded. \n')
appended_data = []

if __name__ == "__main__":
    #for validating MIS with the bb.txt file
    for classname,elements in file.validation.items():
        files = file.validation[classname]
        classname = my_validation(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:    
            merged = my_validation.comparison(classname,master,"Account_Num","Account_No")
            dfs = my_validation.odtl_check(merged,'Balance','M_Bnm_Balance')
            appended_data.append(dfs)
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1
    print("================================")         
    appended_data = pd.concat(appended_data)


print(appended_data.shape)