from my_files import*
from my_classes import*
from main import*
master =  file.master
code_ref = file.code_ref
bullet = 1
master_BC = []

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
            master_BC.append(dfs)
        except Exception as e:
            print(f"        File {files['filename']} is not compatible \n        !! {e} is not found")
            pass
        bullet = bullet + 1   
    master_BC = pd.concat(master_BC,sort=True).drop_duplicates(subset='Account_No')
    master_BC[['BC_NAME']] = master_BC[['BC_NAME']]\
                            .replace({'JOHOR BARU BC':'JOHOR BAHRU BC'})\
                            .replace({'SUBANG':'SUBANG BC'})
    
    print("================================")  
    for x,j in file.preparation.items():
        classname = x
        files = file.preparation[classname]
        classname = my_transformation(
                    files['filename'],
                    files['sheet'],
                    files['merge_on'],
                    files['check_on'],
                    files['skiprow'])
        print(f"{bullet} . {files['filename']}, {files['sheet']} is loaded")
        print(classname.shape)
        bullet = bullet + 1
        
        if x == 'gil':
            gil = my_transformation.create_column(classname,'PL+GIL','PL')
            gil = my_transformation.tag(gil,'Stage 3 Reason','PL IPL IPL R&R NPL',file.taggings)
            gil = my_transformation.get_gil(gil,'GCIF #','PL IPL IPL R&R NPL','PL+GIL')
        elif x == 'lb_f' or x == 'lb_uf':
            if x =='lb_f':
                lb_f = my_transformation.calculation(classname,'Broad Code','M_Cus_No','NOB')
            else:
                lb_uf = my_transformation.calculation(classname,'Broad Code','M_Cus_No','Nature_of_Business') #renames Nature of business to NOB
        elif x == 'nob':
            nob = my_transformation.get_nob(classname,'NOB Code','Sub Sector Desc','NOB Desc')
    
    """merge gil with master(bb.txt)"""       
    masterbb = my_transformation.do_merge(master,gil,'left','GCIF','GCIF #')\
                .drop(columns=['GCIF #'])
    """merge lb funded with nob"""      
    lb_f = my_transformation.do_merge(lb_f,nob,'left','Broad Code','NOB Code')\
                .drop(columns=['NOB Code'])
    """merge lb notfunded with nob"""      
    lb_uf = my_transformation.do_merge(lb_uf,nob,'left','Broad Code','NOB Code')\
                .drop(columns=['NOB Code'])
    """merge lb funded and lb not funded"""     
    lb_fnf = pd.concat([lb_f,lb_uf],sort=True).drop_duplicates(subset='M_Cus_No')
    """merge masterbb (gil with master(bb.txt)) with lb_fnf"""   
    masterbb1 = my_transformation.do_merge(masterbb,lb_fnf,'left','GCIF','M_Cus_No')
    masterbb2 = my_transformation.do_merge(masterbb1,master_BC,'left','GCIF','Account_No')
    masterbb3 = my_transformation.do_merge(masterbb2,code_ref,'left','BRR','BRR')
  
    print(masterbb3.info())

