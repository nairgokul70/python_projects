__author__ = 'gokul.nair'
def in_fridge ():

 try:
      count = fridge[wanted_food]
 except KeyError:
      count = 0
 return count


