
import signal
import subprocess
import time
import os
import string

nodeid=1

def main():
	while(True):
		os.system("rm foo-01.csv")
	
		pro = subprocess.Popen("airodump-ng mon0 -w ./foo --output-format csv", stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
		time.sleep(5)
		os.killpg(pro.pid,signal.SIGINT)
		#os.killpg(pro.pid,signal.SIGINT)
		pro.wait()
		#time.sleep(5)
		#os.killpg(pro.pid,signal.SIGTERM)	
		time.sleep(1)
	
		foo_file = open("foo-01.csv",'r')
		block = foo_file.read()
		foo_file.close()
		if len(block) > 0:
			#print block
			text = block.split("Probed ESSIDs")[1].strip();
			print "TEXT" + text
			chunks = text.split("\n")

			#print chunks
		
			import mysql.connector
			cnx = mysql.connector.connect(host='talend',user='talend',password='talend123',database='raspberry_pi')
			cursor = cnx.cursor()

			chunks = chunks[0:len(chunks)-2]
			
			if len(chunks)==8:
				for row in chunks:
					row = str(nodeid) + "," + row
					row_chunks = row.split(',')
					row2 = row_chunks[0]
					for i in range(1,7):
						row2 = row2 + "," + row_chunks[i] 
					row2 = row2 + ", "	
					#print "ROW: " + row2
					result = cursor.execute("""INSERT INTO serialdata  SELECT %s,now(),%s,%s,%s,%s,%s,%s,%s""",row2.split(','))

				#for i in result:
				#	print i

				cnx.commit()
				cursor.close()
		else:
			print "ERROR?: foo-01.csv is empty"

	time.sleep(1)

if __name__ == "__main__": 
	main()
