__author__ = 'gokul.nair'
import shutil
import pysvn
import base64
src = "C:\development\\talend\workspace\QA_REVENUE_RECOGNITION\process\Prod\ProcessRejections"
dst = "C:\development\\talend\workspace\DEV_REVENUE_RECOGNITION\process\Prod\ProcessRejections"
filename = "load_revrec_gamelogdailylegacy_rejections_0.1"
def copy_replace():
    shutil.copy(src+"\\"+filename+".item",dst+"\\"+filename+".item")
    shutil.copy(src+"\\"+filename+".properties",dst+"\\"+filename+".properties")
    shutil.copy(src+"\\"+filename+".screenshot",dst+"\\"+filename+".screenshot")
copy_replace()
def check_in():
   def svn_credentials(*args):
       return True, 'talend', base64.b16encode("T@lend2015!"), False
   client = pysvn.Client()
   client.callback_get_login =  svn_credentials
   client.checkin(dst+"\\"+filename+".item","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)
   client.checkin(dst+"\\"+filename+".properties","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)
   client.checkin(dst+"\\"+filename+".screenshot","update the gamelogdailylegacy dev job",recurse=False,keep_locks=False)


