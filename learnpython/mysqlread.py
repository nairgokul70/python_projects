__author__ = 'Gokul.Nair'
'''
import os
cwd=os.getcwd()
print cwd
'''
''' This is a paramiko test module program to copy files on edge node'''

import paramiko
import os
from scp import SCPClient
def createSSHClient(server,port,user,password):
    client=paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server,port,user,password)
    return client

ssh=createSSHClient('vgthadoopcm.vgt.net', 22, 'datascience', 'Analytics14!')
scp = SCPClient(ssh.get_transport())
for (dirname,dirs,files) in os.walk('C:\python_projects\learnpython'):
    for filename in files:
        thefile = os.path.join(dirname,filename)
    scp.put(thefile,'/tmp')

