__author__ = 'gokul.nair'
import os
import sys
import shutil
rootdir = "C:\development\\talend\workspace"

for dirName,subdirList,fileList in os.walk(rootdir):
        for filename in [f for f in fileList if f.__contains__("load_revrec_gameplaylog_rejections_0.1")]:
            if f.__contains__(".item") or f.__contains__(".properties") or f.__contains__("screenshot"):
                   #print dirName,filename
                   def dev_to_qa():
                     qa_dir = ""
                     dev_dir = ""
                     if dirName.__contains__("QA"):
                            qa_dir = dirName
                     elif dirName.__contains__("DEV"):
                            dev_dir = dirName
                     shutil.copy(dev_dir+"\\"+filename,qa_dir+"\\"+filename)


                   def qa_to_dev():
                     qa_dir = ""
                     dev_dir = ""
                     if dirName.__contains__("DEV"):
                            dev_dir = dirName
                     elif dirName.__contains__("QA"):
                            qa_dir = dirName
                     shutil.copy(qa_dir+"\\"+filename,dev_dir+"\\"+filename)
                   qa_to_dev()














