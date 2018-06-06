__author__ = 'gokul.nair'
for i in range(1,100):
    for num in range(2,i):
        if (i%num == 0 and i%i == 0):
            print "The number %i is prime number" % i


