__author__ = 'gokul.nair'
import os
rootdir = "C:\development\\talend\workspace"
jobname = "load_master_processrejections_0.1"
def find_workingdirectory(rootdir,jobname):
    qa_dir = []
    dev_dir = []
    qa_filenames = []
    dev_filenames = []
    for dirName,subdirList,fileList in os.walk(rootdir):
        for filename in [f for f in fileList if f.__contains__(jobname)]:
               if dirName.__contains__("QA"):
                       qa_filenames.append(dirName+"\\"+filename)
                       qa_dir.append(dirName)
               elif dirName.__contains__("DEV"):
                       dev_filenames.append(dirName+"\\"+filename)
                       dev_dir.append(dirName)
    return (qa_filenames,dev_filenames,qa_dir,dev_dir)

qa_filenames,dev_filenames,qa_dir,dev_dir = find_workingdirectory(rootdir,jobname)
qa_set = qa_dir[0]
dev_set = dev_dir[0]
print qa_set
print dev_set
print qa_filenames
print dev_filenames









