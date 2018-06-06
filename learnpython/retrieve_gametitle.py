__author__ = 'gokul.nair'
import csv
import re
with open("C:\\development\\talend\\workspace\\out.csv",'rb') as csvfile:
  reader = csv.reader(csvfile,delimiter=';')
  gametitles = []
  gametitles_doublequote = []
  for row in reader:
        for cell in row:
            #print cell.replace("'","")
            gametitles.append(cell)
print gametitles
gametitles_doublequote.append(', '.join('"{0}"'.format(w) for w in gametitles))
print gametitles_doublequote
file = open("C:\\development\\talend\workspace\\gametitles.txt","w")
file.write(', '.join('"{0}"'.format(w) for w in gametitles))
file.close()