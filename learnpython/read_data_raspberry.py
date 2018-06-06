__author__ = 'gokul.nair'
import csv
import mysql.connector
cnx = mysql.connector.connect(host='talend',user='talend',password='talend123',database='raspberry_pi')
cursor = cnx.cursor()

csv_data = csv.reader(file('c:\winpython\WinPython-64bit-2.7.10.1\csv\\birth1880.csv'))
csv_data.next()
for row in csv_data:
    cursor.execute("""INSERT INTO serialdata SELECT %s,%s,%s,%s,%s,%s,%s""",row)

cnx.commit()
cursor.close()
print "Done"



