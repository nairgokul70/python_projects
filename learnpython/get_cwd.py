__author__ = 'gokul.nair'
import os
import base64
import shutil
import pysvn
rootdir = "C:\development\\talend\workspace"
jobname = "load_master_processrejections_0.1"



def checkin(dst,jobname):
       def svn_credentials(*args):
                 return True, 'talend',"T@lend2015!", False
       client  = pysvn.client()
       client.callback_get_login = svn_credentials
       try:
          client.checkout("http://talend.vgt.net/talend_projects/DEV/trunk/process/Prod/ProcessRejections/"+jobname+".item","C:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\Prod\ProcessRejections\\"+jobname+".item")
          client.checkout("http://talend.vgt.net/talend_projects/DEV/trunk/process/Prod/ProcessRejections/load_revrec_gamecashinfolog_rejections_0.1.item","C:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\Prod\ProcessRejections\\"+jobname+".properties")
          client.checkout("http://talend.vgt.net/talend_projects/DEV/trunk/process/Prod/ProcessRejections/load_revrec_gamecashinfolog_rejections_0.1.item","C:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\Prod\ProcessRejections\\"+jobname+".screenshot")
          print "Finished --checkout"
       except Exception, e:
          print 'Failed checkout', e
          raise
       try:
          client.checkin(dst+"\\"+jobname+".item","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)
          client.checkin(dst+"\\"+jobname+".properties","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)
          client.checkin(dst+"\\"+jobname+".screenshot","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)
          print "Finished --checkin"
       except Exception, e:
          print 'Failed checkin', e
          raise

def find_workingdirectory(rootdir,jobname):
    qa_dir = ""
    dev_dir = ""
    for dirName,subdirList,fileList in os.walk(rootdir):
        for filename in [f for f in fileList if f.__contains__(jobname+".item")]:
               if dirName.__contains__("QA"):
                      qa_dir = dirName
               elif dirName.__contains__("DEV"):
                      dev_dir = dirName
    return (qa_dir,dev_dir)

qa_dir,dev_dir = find_workingdirectory(rootdir,jobname)
def qa_to_dev_and_checkin(qa_dir,dev_dir,jobname):
    dst = dev_dir
    shutil.copy(qa_dir+"\\"+jobname+".item",dev_dir+"\\"+jobname+".item")
    shutil.copy(qa_dir+"\\"+jobname+".properties",dev_dir+"\\"+jobname+".properties")
    shutil.copy(qa_dir+"\\"+jobname+".screenshot",dev_dir+"\\"+jobname+".screenshot")
    #checkin(dst,jobname)

qa_to_dev_and_checkin(qa_dir,dev_dir,jobname)
























