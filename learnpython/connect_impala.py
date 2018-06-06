from impala.dbapi import connect
import argparse
import sys

impalanode="vgthadoopdn1.vgt.net"
impalaport=21050

parser = argparse.ArgumentParser()
parser.add_argument('-d',action="store",dest="db")
parser.add_argument('-t',action="store",dest="tb")
param = parser.parse_args()

conn = connect(host=impalanode, port=impalaport, auth_mechanism="GSSAPI", timeout=900)
cursor = conn.cursor()
cursor.execute("refresh `%s`.`%s`" % (param.db,param.tb))

