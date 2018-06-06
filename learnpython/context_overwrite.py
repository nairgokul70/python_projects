__author__ = 'gokul.nair'

import os
import os.path
import xml.etree.ElementTree as ET
import mysql.connector

path = "c:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\\"
cnx = mysql.connector.connect(host='talend',user='talend',password='talend123',database='talend')
cursor = cnx.cursor()
for dirpath, dirnames, filenames in os.walk(path):
    for filename in [f for f in filenames if f.endswith(".item")]:
        tree = ET.parse(dirpath+"\\"+filename)
        root = tree.getroot()
        for child in root.findall('context'):
          for contextparameter in child:

              contextparametername = contextparameter.get('name')
              contextparametervalue = contextparameter.get('value')
              add_context = """INSERT INTO contexts
                               SELECT %s,%s,%s"""

              datavalues = (filename,contextparametername,contextparametervalue)
              cursor.execute(add_context,datavalues)
              cnx.commit()
cursor.close()
cnx.close()
