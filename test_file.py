from my_files import*
from my_classes import*
import itertools
path = os.path.dirname(os.path.realpath(__file__))
master =  file.master
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
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        print(classname.shape)
        bullet = bullet + 1
        
        if x == 'gil':
            gil = my_transformation.tag(classname,'Stage 3 Reason','PL IPL IPL R&R NPL')
        elif x == 'lb_f' or x == 'lb_uf':
            if x =='lb_f':
                lb_f = my_transformation.calculation(classname,'Broad Code','M_Cus_No','NOB')
            else:
                lb_uf = my_transformation.calculation(classname,'Broad Code','M_Cus_No','Nature_of_Business') #renames Nature of business to NOB
        elif x == 'nob':
            nob = my_transformation.my_slicer(classname,'NOB','Sub Sector Desc','NOB Desc')


