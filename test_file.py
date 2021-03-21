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
        # my_transformation.tagging(files['filename'],files['sheet'],files['merge_on'],files['check_on'],files['skiprows'])
        # classname = my_automation.tagging(files['filename'],files['sheet'],files['merge_on'],files['check_on'],files['skiprows'])
        classname = my_transformation(
                    files['filename'],
                    files['sheet'],
                    files['merge_on'],
                    files['check_on'],
                    files['skiprow'])
        if x == 'gil':
            print("boiiii")
        elif x == 'lb_f':
            print("BIg boiii")

    