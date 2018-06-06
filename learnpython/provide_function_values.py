__author__ = 'gokul.nair'
def in_fridge(some_fridge,desired_item):
    try:
        count = some_fridge[desired_item]
    except KeyError:
        count = 0
    print count


fridge = {'apples':10,'oranges':3,'milk':2}
wanted_food = "milk"
in_fridge(fridge,wanted_food)









