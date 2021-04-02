import random
from datetime import datetime

my_dictionary = {}
mylist = []


def give_date():
    y = str(random.randint(1963, 2020))
    m = str(random.randint(1, 12)).zfill(2)  # rjust and ljust
    d = str(random.randint(1, 31)).zfill(2)
    date = y + m + d
    return date


for i in range(11):
    date = give_date()
    amount = random.randint(1000, 9999)
    my_dictionary.update({"trans_date": date, "trans_amount": amount})
    mylist.append(my_dictionary.copy())

print(mylist[1])
x = datetime.strptime(str(mylist[1]["trans_date"]), "%Y%m%d")
print(x)

for i in mylist:
    x = datetime.strptime(str(mylist[i]["trans_date"]), "%Y%m%d")
    print(x)


# for x in mylist:
#     z =mylist[x]["trans_date"]
#     print