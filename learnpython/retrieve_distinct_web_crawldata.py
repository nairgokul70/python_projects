__author__ = 'gokul.nair'
file = open("C:\\Users\\gokul.nair\\Desktop\\2017-05-12T095430out.txt","r")
#print file.read()
mylist = []
mylist.append(file.read())
mynewlist = []
#print mylist
#myset = list(set(mylist))
#mynewlist = list(myset)


#file = open("C:\\Users\\gokul.nair\\Desktop\\crawloutput.txt", "w")
for i in mylist:
    if i not in mynewlist:
        mynewlist.append(i)
        print i


#file.close()

#
#file.write(mylist)
