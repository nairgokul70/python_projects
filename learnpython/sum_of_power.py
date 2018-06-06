__author__ = 'gokul.nair'
sum_value = []
from math import pow
value = long(pow(2,1000))
for i in str(value):
    sum_value.append(int(i))
    #print(i)
print(sum(sum_value))
#newestvalue = long(sum_value)
#print(sum(newestvalue))

