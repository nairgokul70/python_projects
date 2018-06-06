__author__ = 'Gokul.Nair'
import MySQLdb,sys
from prettytable import from_db_cursor
def mysqlexceptionhandling(identifier):
    mydb = MySQLdb.connect(host='vgthadoopcm',user='hive',passwd='vgthadoop',db='metastore')
    cur=mydb.cursor()
    statement="""SELECT TBL_ID,DB_ID,OWNER,TBL_NAME,TBL_TYPE FROM TBLS WHERE TBL_TYPE='%s'"""%(identifier)
    while True:
              try:
                  print "\nTrying SQL Statement: %s" %(statement)
                  cur.execute(statement)
                  '''results=cur.fetchall()'''
                  print "The results of the query are:"
                  pt=from_db_cursor(cur)
                  print pt
                  break
              except (MySQLdb.Error,MySQLdb.Warning):
                  new_id = raw_input("The TBL_TYPE you entered is not valid. please enter a valid TBL_TYPE")

mysqlexceptionhandling('EXTERNAL_TABLE')

