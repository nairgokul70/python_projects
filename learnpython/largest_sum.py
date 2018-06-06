__author__ = 'gokul.nair'
from itertools import islice
complete_string = []
part_string = []
with open('C:\python_files\largest_sum.txt','r') as f:
        for line in f:
            lines = line.rstrip('\n')
            complete_string.append(long(lines))
            #for lines in complete_string:
                #part_string.append(int(lines[0:10]))
value = str(sum(complete_string))
print(value[0:10])
        #print(complete_string)
        #print(complete_string[1][0:10])





