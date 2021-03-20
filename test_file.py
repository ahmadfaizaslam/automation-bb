import itertools
from my_files import*

for filename, sheet in ( 
        itertools.chain.from_iterable( 
            [itertools.product((k, ), v) for k, v in file.validation.items()])): 
                print(filename)
                print(sheet)