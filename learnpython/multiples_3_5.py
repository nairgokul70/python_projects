__author__ = 'gokul.nair'
multiples = []

for num in range(1,10):
    if((num%3==0) or (num%5==0)):
       multiples.append(num)
       print(multiples)

print(sum(multiples))





