__author__ = 'gokul.nair'
import os
import pysvn
import string
import shutil
rootdir = "C:\development\\talend\workspace"
jobname = ["load_master_processrejections_hadoop_0.1","load_revenue_recognition_0.1"]

def svn_credentials(*args):
    return True, 'gokul.nair',"Talend2015!", False
client = pysvn.Client()



src = "DEV_REVENUE_RECOGNITION"
dst = "DEV_DZ"
src_files = []
dst_files = []
for fname in jobname:
   for dirName,subdirList,fileList in os.walk(rootdir):
        for filename in [f for f in fileList if f.__contains__(fname)]:
            if dirName.__contains__(src):
               src_files.append(dirName+"\\"+filename)
               #print dirName+"\\"+filename


def copy_replace_file():
 for src_file_name in src_files:
        srcfilename = src_file_name
        dstfilename = string.replace(srcfilename,src,dst)
        dst_files.append(dstfilename)
        if os.path.isfile(dstfilename):
         print "file exists, locking file %s for overwriting" %(dstfilename)
         #client.lock(dstfilename,"locked for change",force=True)
         client.lock(dstfilename,force=True)
        else:
         print "file does not exist. copying file %s and checkin will happen" %(dstfilename)


        #shutil.copy(srcfilename,dstfilename)
        #client.checkin(dstfilename,"updated the job with new changes",recurse=False,keep_locks=False)
 return dst_files



output_files = copy_replace_file()
print output_files



#def check_in(dst,jobname):







#print dev_dir








#copy_replace_file()









