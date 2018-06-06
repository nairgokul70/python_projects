class Row:

    def __init__(self, key, line):
        #line = inline.split(',')
        self.key = key
        self.nodeid = line[0]
        self.scantime = line[1]
        self.station_mac = line[2]
        self.first_time_seen = line[3]
        self.last_time_seen = line[4]
        self.pwr = line[5]
        self.packets = line[6]
        self.BSSID = line[7]
        self.probed_ESSIDS = line[8]
        self.used = False

class Group:
    def __init__(self):
        self.rows = []



import mysql.connector


def main():
        cnx = mysql.connector.connect(host='talend',user='talend',password='talend123',database='raspberry_pi')
        cursor = cnx.cursor()
        #cursor.execute("""Truncate table scanned_serialdata""")

        # results = cursor.execute("""select SD.nodeid,SD.station_mac,SD.scantime,SD.pwr,minscantime,maxscantime from
        # (select DISTINCT scantime,nodeid,station_mac,pwr from serialdata) SD
        # INNER JOIN
        # (select date_sub(max(scantime),INTERVAL 10 SECOND) as minscantime,max(scantime) as maxscantime,
        # station_mac from serialdata GROUP BY station_mac) MMSC
        # ON ltrim(rtrim(SD.station_mac)) = ltrim(rtrim(MMSC.station_mac))
        # AND SD.scantime  >= MMSC.minscantime and SD.scantime <= MMSC.maxscantime""")

        #results = cursor.execute("describe serialdata")
        results = cursor.execute("select * from serialdata")

        rows = []
        i = 0
        for line in cursor:
            print "LINE: " + str(line)
            rows.append(Row(i, line))
            i += 1

        groups = []
        kmax = 0
        k = 0
        i = 0
        for i in range(0, len(rows)-1):
            if not rows[i].used:
                tempgroup = Group()
                tempgroup.rows.append(rows[i])
                #print rows[i].scantime
                #print (rows[i+1].scantime - rows[i].scantime).seconds
                #start_time = rows[i].scantime
                for k in range(i+1, len(rows)-1):
                    diff_secs = (rows[k].scantime - rows[i].scantime).seconds
                    if diff_secs < 10 and (not rows[k].used) and rows[i].station_mac == rows[k].station_mac:
                        found = False
                        for row in tempgroup.rows:
                            if row.nodeid == rows[k].nodeid:
                                found = True
                                break
                        if not found:
                            tempgroup.rows.append(rows[k])
                    else:
                        break

                if len(tempgroup.rows) == 3:
                    rows[tempgroup.rows[0].key].used = True
                    rows[tempgroup.rows[1].key].used = True
                    rows[tempgroup.rows[2].key].used = True
                    print "Group: %s-%s:%s %s-%s:%s %s-%s:%s" % \
                          (tempgroup.rows[0].key, tempgroup.rows[0].nodeid, tempgroup.rows[0].scantime,
                           tempgroup.rows[1].key, tempgroup.rows[1].nodeid, tempgroup.rows[1].scantime,
                           tempgroup.rows[2].key, tempgroup.rows[2].nodeid, tempgroup.rows[2].scantime)
                    groups.append(tempgroup)



        #query = ("""SELECT station_mac,pwr,nodeid FROM scanned_serialdata SD WHERE SD.station_mac
        #       in (select station_mac from scanned_serialdata group by station_mac having
        #         count(distinct nodeid) >= (select count(distinct nodeid) from nodes))""")

        # cursor.execute(query)
        output_string = ""
        for group in groups:
            for row in group.rows:
                if row.nodeid == 1:
                    pwr1 = row.pwr
                elif row.nodeid == 2:
                    pwr2 = row.pwr
                elif row.nodeid == 3:
                    pwr3 = row.pwr

            #if pwr1 <> '' and pwr2 <> '' and pwr3 <> '':
            #os.system("python tri.py 100 50 86.5 %s %s %s" % (pwr1, pwr2, pwr3))
            from python_projects.learnpython import tri
            #print tri.main(("100", "50", "86.5", str(pwr1), str(pwr2), str(pwr3)))

            output_string += "%s,%s," % (group.rows[0].station_mac, group.rows[0].scantime) + \
                             tri.main(("100", "50", "86.5", str(pwr1), str(pwr2), str(pwr3)))

        print output_string.strip()
        f = open("drone_output.csv", 'w')
        f.write(output_string)
        f.close()

        cnx.commit()
        cnx.close()


if __name__ == "__main__":
    main()




