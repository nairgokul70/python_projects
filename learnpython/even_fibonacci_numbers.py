def recur_fibo(n):
   """Recursive function to
   print Fibonacci sequence"""
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))


# take input from the user
nterms = 10
even_numbers = []
# check if the number of terms is valid
if nterms <= 0:
   print("Plese enter a positive integer")
else:
   print("Fibonacci sequence:")
   for i in range(nterms):
       if (recur_fibo(i)%2) ==0:
          even_numbers.append(recur_fibo(i))
       print(recur_fibo(i))
       print(even_numbers)