__author__ = 'gokul.nair'
import mysql.connector
cnx = mysql.connector.connect(host='talend',user='talend',password='talend123',database='talend')
cursor = cnx.cursor()
query = ("select filename,inserteddate,iscurrent from nonrepofilenames limit 1")
cursor.execute(query)
for (filename) in cursor:
    print filename
cursor.close()
cnx.close()

