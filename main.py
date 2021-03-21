import pandas as pd
import os
from my_classes import*
from my_files import*
import itertools

bullet = 1
master =  file.master
print('\n Master file loaded. \n')


if __name__ == "__main__":
    
    for x,y in file.validation.items():
        files = file.validation[x]
        classname = my_automation(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:    
            merged = my_automation.comparison(classname,master,"Account_Num","Account_No")
            my_automation.odtl_check(merged,'Balance','M_Bnm_Balance')
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1
                
                
               
    # z = my_automation.ccnt(classname,'M_Cus_No','BC_NAME','REGION')
    # ww.update(z)
    
# print(z.shape)