__author__ = 'gokul.nair'
deltacount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 0, -4, 0, -3, 3, 0, -12, -8, 0, 0, 0, 0, 0, 0, -20, 0, 0, -6, 0]
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 0, -4, 0, -3, 3, 0, -12, -8, 0, 0, 0, 0, 0, 0, -20, 0, 0, -6, 0]
#[0, -7, 0, 0, -8, 0, 0, -4, 0, 0, 0, -6, 0, -4, -29, -10, 0, -16, 0, 0, 2, 3, 0, 18, -1, -2, 0, 0, 0, 0, 0, 0, 21, 10, -10, 0, -12, 0]


zero_before_count=0
zer_after_count=0
indx=0
list1=[]
list2=[]
list3 = []
index_raw = []
print len(deltacount)

for indx,i in enumerate(deltacount):
    try:
         if i!= 0:
            list2.append(indx)
            if deltacount[indx - 1] == 0 and deltacount[indx - 2] == 0:
                      if deltacount[indx + 1] == 0 and deltacount[indx + 2] == 0:
                          list1.append(i)
    except IndexError:
       pass
       continue

finallist=[x for x in list2 if x not in list1 and x!=0]
print deltacount
print list1
print list2
print finallist


'''
for indx,i in enumerate(deltacount):
    #print indx,deltacount[indx],deltacount[indx + 1],deltacount[indx + 2]
    if deltacount[indx+1] != 0:

'''


'''
    if i!= 0:
      list2.append(indx)
    if len(deltacount[indx+2]):
      if deltacount[indx - 1] == 0 and deltacount[indx - 2] == 0:
             if deltacount[indx + 1] == 0 and deltacount[indx + 2] == 0:
                list1.append(i)


finallist=[x for x in list2 if x not in list1 and x!=0]
print deltacount
print list1
print list2
print finallist
'''


'''
    if i!=0:
        indx=deltacount.index(i)
        if deltacount[indx-1]==0 and deltacount[indx-2]==0:
            if deltacount[indx+1]==0 and deltacount[indx+2]==0:

                list1.append(i)
finallist=[x for x in deltacount if x not in list1 and x!=0]
print finallist
'''



