import pandas as pd
import os
from my_classes import*
from my_files import*
import itertools

x = 1
master =  file.master
print('Master file loaded.')

if __name__ == "__main__":
    for filename, sheet in ( 
        itertools.chain.from_iterable( 
            [itertools.product((filename, ), sheet) for filename, sheet in file.validation.items()])): 
                print()
                classname = filename.replace(" ","")
                classname = my_automation(filename,sheet)
                print(f"{x} . {filename},{sheet} is loaded")
                try:    
                    merged = my_automation.comparison(classname,master,'Account_Num','Account_No')
                    my_automation.odtl_check(merged,'Balance','M_Bnm_Balance_SUM1')
                except Exception as e:
                        print(f"        File {filename} is not compatible \n        !! {e} is not found")
                        pass     
                x = x +1
                
                
               
    # z = my_automation.ccnt(classname,'M_Cus_No','BC_NAME','REGION')
    # ww.update(z)
    
# print(z.shape)