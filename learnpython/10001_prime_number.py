__author__ = 'gokul.nair'
import time
start_time = time.clock()

#I break the loop if any of the numbers in div_by divide evenly, because that means x is not prime
#If it gets through all the numbers without having an even divisor, it returns true
def is_prime(x):
    div_by = [i for i in range(2, int(x ** 0.5) + 1)]
    for i in div_by:
        if x % i == 0:
            break
    else:
        return True

#For this bit I will start at 2, test for primality, and if it passes, I will append it to a list of primes and then check the next number.
#If the list reaches to 10,001 items I will break the loop
primes = []
test = 2
while True:
    if is_prime(test):
        primes.append(test)
    if len(primes) == 10001:
        break
    test += 1

#I printed part of this list to make sure it was working properly
print('prime list check:', primes[:10])
print('the number of primes found:', len(primes))
print('the 10001st prime:', primes[10000])

print()
print('finished in:', time.clock() - start_time, 'seconds')

