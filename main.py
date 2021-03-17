import pandas as pd
import os
from my_functions2 import*
from my_files import*

path = file.dir_path    
master =  file.master
print('Master file loaded completed.')



if __name__ == '__main__':
    x1 = my_comparison("STRC FY 1112 product table 1","STRC_BB_monthly_4")
    try:    
        x2 = my_comparison.comparison(x1,master,'Account_Num','Account_No')
        my_comparison.odtl_check(x2,'Balance','M_Bnm_Balance_SUM1')
    except Exception as e:
            print(f"    File dataframe is not compatible \n   !! {e} is not found \n")
            print('___________________________')
            pass
    
    