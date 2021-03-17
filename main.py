import pandas as pd
import os
from my_classes import*
from my_files import*
x = 1
master_BC = {}
master =  file.master
print('Master file loaded.')

for filename,sheet in file.validation.items():
    print()
    classname = filename.replace(" ","")
    classname = my_comparison(filename,sheet)
    print(f"{x} . {filename} is loaded")
    try:    
        merged = my_comparison.comparison(classname,master,'Account_Num','Account_No')
        my_comparison.odtl_check(merged,'Balance','M_Bnm_Balance_SUM1')
    except Exception as e:
            print(f"        File dataframe is not compatible \n        !! {e} is not found")
            pass
    x = x +1
    c = my_comparison.ccnt(classname,'M_Cus_No','BC_NAME','REGION')
    master_BC.update(c)

print(type(master_BC))
    
    
   