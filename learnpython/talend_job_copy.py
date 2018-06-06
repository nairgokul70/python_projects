__author__ = 'gokul.nair'
import pysvn
import os
import shutil
rootdir = "C:\development\\talend\workspace"
jobname = ["load_master_processrejections_hadoop_0.1","load_revenue_recognition_0.1"]

# Find the working QA , DEV & PROD working directory
#def find_workingdirectory(rootdir,jobname):
#
def find_workingdirectory(rootdir,jobname):
 qa_dir = set() ; dev_dir = set() ; prod_dir = set() ; qa_files = [] ; dev_files = [] ; prod_files = []
 for fname in jobname:
   for dirName,subdirList,fileList in os.walk(rootdir):
         for filename in [f for f in fileList if f.__contains__(fname)]:
              if dirName.__contains__("QA"):
                      qa_dir.add(dirName)
                      qa_files.append(dirName+"\\"+filename)
              elif dirName.__contains__("DEV"):
                      dev_dir.add(dirName)
                      dev_files.append(dirName+"\\"+filename)
              elif dirName.__contains__("REV"):
                      prod_dir.add(dirName)
                      prod_files.append(dirName+"\\"+filename)
 return(qa_dir,dev_dir,prod_dir,qa_files,dev_files,prod_files)

qa_dir,dev_dir,prod_dir,qa_files,dev_files,prod_files = find_workingdirectory(rootdir,jobname)

print qa_files
print dev_files

#def copy_replace_files(dir_files,qa_files):






