from my_classes import *


# for x, y in file.funded.items():
#     print(x,y)


# masterbb3 = my_transformation.conditional_copy(masterbb3,'PL+GIL','Risk Cat CRD','GIL','GIL')

# masterbb3 = my_transformation.conditional_copy(masterbb3,'PL IPL IPL R&R NPL','Risk Cat GCMC','IPL','IPL')
# masterbb3 = my_transformation.conditional_copy(masterbb3,'PL IPL IPL R&R NPL','Risk Cat GCMC','IPL R&R','IPL R&R')
# masterbb3 = my_transformation.conditional_copy(masterbb3,'PL IPL IPL R&R NPL','Risk Cat GCMC','NPL','NPL')
    
for var in [('IPL'),('IPL R&R'),('NPL')]:
    print(f"masterbb3 = my_transformation.conditional_copy(masterbb3,'PL IPL IPL R&R NPL','Risk Cat GCMC',{var},{var})")
    