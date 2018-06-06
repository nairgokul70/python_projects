__author__ = 'gokul.nair'
import xml.etree.ElementTree as ET
tree = ET.parse("c:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\Prod\load_revenue_recognition_0.1.item")
root = tree.getroot()
for child in root.findall('context'):
    for contextparameter in child:
        contextparametername = contextparameter.get('name')
        contextparametervalue = contextparameter.get('value')
        print contextparametername,contextparametervalue







