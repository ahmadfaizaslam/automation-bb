import pandas as pd
from pandas.core.reshape.concat import concat
from my_classes import*
from my_files import*
master_bc_gcif= []
master_bc_acc= []
bullet = 1
master =  file.master



print('\n Master file loaded. \n')

if __name__ == "__main__":
    #for validating MIS with the bb.txt file
    for classname,elements in file.validation.items():
        x = classname
        files , frame = file.validation[classname] , classname
        classname = my_validation(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:    
            merged = my_validation.comparison(classname,master,"Account_Num","Account_No")
            print("After mergin with bb.txt",merged.shape)
            dfs = my_validation.odtl_check(merged,'Balance','M_Bnm_Balance')
            dfs = dfs[['Account_No','BC_NAME','REGION']]
            if x == 'strc_bc' or x == 'trade_nf' or x =='trade_f':
                master_bc_gcif.append(dfs)
            else:
                master_bc_acc.append(dfs)
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1   
    master_bc_gcif = pd.concat(master_bc_gcif,sort=True)
    master_bc_acc = pd.concat(master_bc_acc,sort=True)
    
    print(master_bc_gcif.info())
    print(master_bc_acc.info())
    print("================================")  