__author__ = 'gokul.nair'
squares = []
squaresum = []
for num in range(1,101):
    value = num * num
    squares.append(value)
    squaresum.append(num)
print(sum(squares))
print((sum(squaresum) * sum(squaresum)))


