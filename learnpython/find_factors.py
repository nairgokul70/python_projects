__author__ = 'gokul.nair'
for num in range(10,21):
    for i in range(2,num):
         if num % i == 0:
           j=num/i          #to calculate the second factor
           print ' %d * %d equals %d' % (num,i,j)
           break
    else:
        print "the number %d is prime number " %num


