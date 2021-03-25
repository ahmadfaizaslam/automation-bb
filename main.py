import pandas as pd
from my_classes import*
from my_files import*
dfs_1= []
dfs_2= []
bullet = 1
master =  file.master



print('\n Master file loaded. \n')

if __name__ == "__main__":
    #for validating MIS with the bb.txt file
    for classname,elements in file.validation.items():
        files , frame = file.validation[classname] , classname
        classname = my_validation(files['filename'],files['sheet'],files['merge_on'],files['check_on'])
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:    
            merged = my_validation.comparison(classname,master,"Account_Num","Account_No")
            #print("After mergin with bb.txt",merged.shape)
            dfs = my_validation.odtl_check(merged,'Balance','M_Bnm_Balance')
             
            # mis_dfs.append(dfs)
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1
          
    # mis_dfs = pd.concat(mis_dfs)
    # mis_dfs = mis_dfs[['Account_No','BC_NAME','REGION']].astype(str) #this will merge to masterbb1
    # print(mis_dfs.info())
    print("================================")  