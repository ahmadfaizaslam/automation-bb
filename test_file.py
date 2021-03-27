from my_files import*
from my_classes import*
import itertools
path = os.path.dirname(os.path.realpath(__file__))
master =  file.master
codes = file.codes
bullet = 1

if __name__ == "__main__":
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
            
    masterbb = my_transformation.do_merge(master,gil,'left','GCIF','GCIF #') 
    lb_f = my_transformation.do_merge(lb_f,nob,'left','Broad Code','NOB Code')
    lb_uf = my_transformation.do_merge(lb_uf,nob,'left','Broad Code','NOB Code')
    lb_fnf = pd.concat([lb_f,lb_uf],sort=True).drop_duplicates(subset='M_Cus_No')
    
print(lb_fnf.info())
