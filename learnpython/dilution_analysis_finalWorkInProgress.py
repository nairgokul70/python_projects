# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:33:35 2016 by jie.zhao
Revised on Tues Mar 1 12:52:33 2016 by ian.burchett

@author: jie.zhao, ian.burchett
"""

import os
import csv
from os import path
import jpype

threshN = input('Please input number of machines increase required to initiate a dilution event (i.e. 25): ')
preN = input('Please input number of months BEFORE a dilution event, to analyze (i.e. 12): ')
postN = input('Please input number of months AFTER a dilution event, to analyze (i.e. 12): ')

print "Pulling raw data from Discovery Zone on Vertica, please wait..."

#load data from Vertica
from jaydebeapi import connect
connection = connect('com.vertica.jdbc.Driver',['jdbc:vertica://vertica01/vgt_edw','TB_temp','tbtemp'],'vertica-jdbc.jar')
cur = connection.cursor()
cur.execute("SELECT * FROM dz.vw_dilution where customernumber = 'CHER002' ORDER BY customernumber, year, month")
results = cur.fetchall()

output = ""
for result in results:
    line = ""
    for part in result:
        line = line + str(part) + ","
    line = line[0:len(line)-1]

    if len(output) > 0:
        output = output + '\n' + line
    else:
        output = line

header = ""
descs = cur.description
for desc in descs:
    column_name = desc[0]
    if len(header) > 0:
        header = header + ',' + column_name
    else:
        header = column_name
output = header + '\n' + output

output = output.replace(".0,", ",")
outfile = open("raw_dilution.csv", 'w')
outfile.write(output)
outfile.close()

files = [f for f in os.listdir("./") if path.isfile(f)]
csv_files = []
for xfile in files:
    if ".csv" in xfile and "_output.csv" not in xfile:
        csv_files.append(xfile)

print "Processing data..."

xfile = "raw_dilution.csv"
f=open(xfile)
csv_f=csv.reader(f)
datraw=[]
for row in csv_f:
    datraw.append(row) # now all the information is stored in
# simplify the data to only customer number[0], customername[1], year[2], month[3],
# beginfootprint[4],deltaptcount[5], actualwin[8],theowin[9],machinedays[10]

#create new dat that contains only the essential variables
namesraw=datraw[0]
names=[namesraw[0],namesraw[1],'year-month',namesraw[4],namesraw[5],namesraw[7],namesraw[8],namesraw[9],namesraw[10],namesraw[11],namesraw[12],namesraw[13]]
dat=[]
customerlistraw=[]
for row in datraw[1:]:
    if row[8]!='0':
        row_temp=[row[0],row[1],row[2]+'-'+row[3],row[4],row[5],row[7],row[8],row[9],row[10],row[11],row[12],row[13]]
        dat.append(row_temp)
        customerlistraw.append(row[0])
datn=len(dat)
# let's create nested list!!! i'm excited? meh~
    # store the customer categorized list in dat_customer
dat_customer0=[]    # find the unique customers in the data sets
customerlist=[]
for ii in range(0,datn):
    if customerlistraw[ii] not in customerlist:
        customerlist.append(customerlistraw[ii])
customer_n=len(customerlist) # this is the number of customers in the data sets
jj=0
dat_customer_temp=[]
for ll in range(0,datn):
    dat_temp=dat[ll]
    if jj<customer_n:
        if dat_temp[0]==customerlist[jj]:
            dat_customer_temp.append(dat_temp)
        else:
            jj=jj+1
            dat_customer0.append(dat_customer_temp)
            dat_customer_temp=[]
dat_customer0.append(dat_customer_temp)
dat_customer = [x for x in dat_customer0 if x != []]

# parameters to specify that customize the qurying result.
#threshN=25
#preN=12
#postN=12
customer_dic=[] # the list that stores of dic_customer{} that stores all info for each customer
df_dic=[]
df_list=[]

for zz in range(0,len(dat_customer)):
    customer=dat_customer[zz] # one of dat records by customer
    customerN=len(customer)   # number of records related to one customer
    dic_customer={}
    customer_temp=customer[0]
    dic_customer[names[0]]=customer_temp[0]
    dic_customer[names[1]]=customer_temp[1]
    time_vec=[]
    beginEGM_vec=[]
    deltaptcount_vec=[]
    gamesplayed_vec=[]
    adjgamesplayed_vec=[]
    theowin_vec=[]
    adjtheowin_vec=[]
    actualwin_vec=[]
    adjactualwin_vec=[]
    machinedays_vec=[]
    for customer_temp in customer:
        time_vec.append(customer_temp[2])
        beginEGM_vec.append(int(customer_temp[3]))
        deltaptcount_vec.append(int(customer_temp[4]))
        gamesplayed_vec.append(int(customer_temp[5]))
        actualwin_vec.append(float(customer_temp[6]))
        theowin_vec.append(float(customer_temp[7]))
        machinedays_vec.append(int(customer_temp[8]))
        adjgamesplayed_vec.append(float(customer_temp[9]))
        adjactualwin_vec.append(float(customer_temp[10]))
        adjtheowin_vec.append(float(customer_temp[11]))
    
    dic_customer[names[2]]=time_vec
    dic_customer[names[3]]=beginEGM_vec
    dic_customer[names[4]]=deltaptcount_vec
    dic_customer[names[5]]=gamesplayed_vec
    dic_customer[names[6]]=actualwin_vec
    dic_customer[names[7]]=theowin_vec
    dic_customer[names[8]]=machinedays_vec
    dic_customer[names[9]]=adjgamesplayed_vec
    dic_customer[names[10]]=adjactualwin_vec
    dic_customer[names[11]]=adjtheowin_vec

    customer_dic.append(dic_customer)

    print("DeltaPTCount_Vec: " + str(deltaptcount_vec))

    # now let's come to the core of calculating the before and after effect...
        # extract info from
    count_temp=0
    index_raw=[]
    index_group=[]
    count=[]
    countContinuousZeros = 1
    for kk,item in enumerate(deltaptcount_vec):
        if item == 0:
            countContinuousZeros = countContinuousZeros + 1
        print("Item: " + str(item) + "CountZeros " + str(countContinuousZeros) )       ## Gokul I have rebuilt index_raw to be only groupings of interest: an index to the values in deltaptcount so you can add up values between first and second index
        if item!=0 and countContinuousZeros >1:
            index_raw.append(kk)
            countContinuousZeros = 0
        
    print("Index_raw: " + str(index_raw))
    index_group=[]
    if index_raw!=[] and (0 not in theowin_vec):
        index_group.append(index_raw[0])
        for mm in range(1,len(index_raw)):
            index_group.append(index_raw[mm]-index_raw[mm-1])

        # group the machine change data based on time intervals.
            ##1. find the adjacent machine count: give the ones the same group number
        print("Index_group : " + str(index_group))
        group_index=[]
        group_index_temp=[]

        for kk in range(0,len(index_group)):
            if index_group[kk]>1:# group events that don't have gap of machine changes in between; change 1 to 2 if you want to bridge the gap
               group_index.append(group_index_temp)
               group_index_temp=[]
               group_index_temp.append(index_raw[kk])
            else:
               group_index_temp.append(index_raw[kk])
        group_index.append(group_index_temp)

        print("Group Index: " + str(group_index))
            ##2. count the machine change in each group
        groupN=len(group_index)
        deltacount=[]
        for mm in range(0,groupN):
            deltacount.append(sum(deltaptcount_vec[nn] for nn in group_index[mm]))
            ##3. save the group with machine change larger than 25.
        groupf=[]
        deltacountf=[]
        group_startf=[]
        group_endf=[]


        print("groupN " + str(groupN))

        for xx in range(0,groupN):
            groupf_temp=group_index[xx]
            if deltacount[xx]>threshN and groupf_temp[0]>0 and groupf_temp[-1]<customerN-1:
               groupf.append(groupf_temp)
               deltacountf.append(deltacount[xx])
               group_startf.append(groupf_temp[0])
               group_endf.append(groupf_temp[-1])


        print("groupf " + str(groupf))
        print("deltacountf " + str(deltacountf))
        print("group_startf " + str(group_startf))
        print("group_end " + str(group_endf) )
        namesdf=['customernumber','customername','starttime','endtime','beginfootprint'
        ,'afterfootprint','deltaptcount','%EGMchange','preUtilization','adjpreUtilization','postUtilization','adjpostUtilization','preTheoWPUPD','adjpreTheoWPUPD','postTheoWPUPD','adjpostTheoWPUPD',
        'preActualWPUPD','adjpreActualWPUPD','postActualWPUPD','adjpostActualWPUPD','%TheoWchange','adj%TheoWchange','%ActualWchange','adj%ActualWchange','DFtheo','adjDFtheo','DFactual','adjDFactual']

        groupfN=len(groupf)
        for yy in range(0,groupfN):
            groupf_temp=groupf[yy]
            df_dic_temp={}
            df_temp=[]
            df_dic_temp['customernumber']=dic_customer['customernumber']
            df_dic_temp['customername']=dic_customer['customername']
            df_dic_temp['starttime']=time_vec[group_startf[yy]]
            df_dic_temp['endtime']=time_vec[group_endf[yy]]
            df_dic_temp['beginfootprint']=beginEGM_vec[group_startf[yy]]
            df_dic_temp['afterfootprint']=beginEGM_vec[group_endf[yy]]+deltaptcount_vec[group_endf[yy]]
            df_dic_temp['deltaptcount']=deltacountf[yy]
            df_dic_temp['%EGMchange']=float(df_dic_temp['deltaptcount'])/float(df_dic_temp['beginfootprint'])
            if group_startf[yy]>(preN-2):

                print("PreRange:" + str(gamesplayed_vec[group_startf[yy]]) + " Start " +  str(gamesplayed_vec[group_startf[yy]-preN+1]) + " End " +  str(gamesplayed_vec[group_startf[yy]+1]) )
                print(str(gamesplayed_vec[4]) + " " + str(gamesplayed_vec[5]) +  " " + str(gamesplayed_vec[6]) + " " + str(gamesplayed_vec[7]) )
                print(str(sum(gamesplayed_vec[group_startf[yy]-preN+1:group_startf[yy]+1]) ))
                print(str(sum(gamesplayed_vec[4:7]) ))
                df_dic_temp['preTheoWPUPD']=sum(theowin_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])
                df_dic_temp['preActualWPUPD']=sum(actualwin_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])
                df_dic_temp['preUtilization']=sum(gamesplayed_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/14400.0                
                df_dic_temp['adjpreTheoWPUPD']=sum(adjtheowin_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])
                df_dic_temp['adjpreActualWPUPD']=sum(adjactualwin_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])
                df_dic_temp['adjpreUtilization']=sum(adjgamesplayed_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/sum(machinedays_vec[group_startf[yy]-preN+1:group_startf[yy]+1])/14400.0                
            else:
                df_dic_temp['preTheoWPUPD']=sum(theowin_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])
                df_dic_temp['preActualWPUPD']=sum(actualwin_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])
                df_dic_temp['preUtilization']=sum(gamesplayed_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])/14400.0
                df_dic_temp['adjpreTheoWPUPD']=sum(adjtheowin_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])
                df_dic_temp['adjpreActualWPUPD']=sum(adjactualwin_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])
                df_dic_temp['adjpreUtilization']=sum(adjgamesplayed_vec[0:group_startf[yy]+1])/sum(machinedays_vec[0:group_startf[yy]+1])/14400.0

            if group_endf[yy]+postN<customerN:

                print("PostRange:" + str(gamesplayed_vec[group_endf[yy]]) + " Start "  + str(gamesplayed_vec[group_endf[yy]+1]) + " End " +  str(gamesplayed_vec[group_endf[yy]+1+postN]) )

                print(str(gamesplayed_vec[7]) + " " + str(gamesplayed_vec[8]) +  " " + str(gamesplayed_vec[9]) + " " + str(gamesplayed_vec[10]) + " " + str(gamesplayed_vec[11]))
                print(str(sum(gamesplayed_vec[group_endf[yy]+1:group_endf[yy]+1+postN]) ))
                print(str(sum(gamesplayed_vec[7:11]) ))
                
                print(str(gamesplayed_vec[group_endf[yy]+1]) + " " + str(gamesplayed_vec[group_endf[yy]+1+postN]))
                df_dic_temp['postTheoWPUPD']=sum(theowin_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])
                df_dic_temp['postActualWPUPD']=sum(actualwin_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])
                df_dic_temp['postUtilization']=sum(gamesplayed_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/14400.0
                df_dic_temp['adjpostTheoWPUPD']=sum(adjtheowin_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])
                df_dic_temp['adjpostActualWPUPD']=sum(adjactualwin_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])
                df_dic_temp['adjpostUtilization']=sum(adjgamesplayed_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/14400.0                
            else:
                df_dic_temp['postTheoWPUPD']=sum(theowin_vec[group_endf[yy]+1:])/sum(machinedays_vec[group_endf[yy]+1:])
                df_dic_temp['postActualWPUPD']=sum(actualwin_vec[group_endf[yy]+1:])/sum(machinedays_vec[group_endf[yy]+1:])
                df_dic_temp['postUtilization']=sum(gamesplayed_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/14400.0
                df_dic_temp['adjpostTheoWPUPD']=sum(adjtheowin_vec[group_endf[yy]+1:])/sum(machinedays_vec[group_endf[yy]+1:])
                df_dic_temp['adjpostActualWPUPD']=sum(adjactualwin_vec[group_endf[yy]+1:])/sum(machinedays_vec[group_endf[yy]+1:])
                df_dic_temp['adjpostUtilization']=sum(adjgamesplayed_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/sum(machinedays_vec[group_endf[yy]+1:group_endf[yy]+1+postN])/14400.0

            df_dic_temp['%TheoWchange']=(df_dic_temp['postTheoWPUPD']-df_dic_temp['preTheoWPUPD'])/df_dic_temp['preTheoWPUPD']
            df_dic_temp['%ActualWchange']=(df_dic_temp['postActualWPUPD']-df_dic_temp['preActualWPUPD'])/df_dic_temp['preActualWPUPD']
            df_dic_temp['DFtheo']= df_dic_temp['%TheoWchange']/df_dic_temp['%EGMchange']
            df_dic_temp['DFactual']= df_dic_temp['%ActualWchange']/df_dic_temp['%EGMchange']
            df_dic_temp['adj%TheoWchange']=(df_dic_temp['adjpostTheoWPUPD']-df_dic_temp['adjpreTheoWPUPD'])/df_dic_temp['adjpreTheoWPUPD']
            df_dic_temp['adj%ActualWchange']=(df_dic_temp['adjpostActualWPUPD']-df_dic_temp['adjpreActualWPUPD'])/df_dic_temp['adjpreActualWPUPD']
            df_dic_temp['adjDFtheo']= df_dic_temp['adj%TheoWchange']/df_dic_temp['%EGMchange']
            df_dic_temp['adjDFactual']= df_dic_temp['adj%ActualWchange']/df_dic_temp['%EGMchange']
            for aa in namesdf:
                df_temp.append(df_dic_temp[aa])
            df_list.append(df_temp)
            df_dic.append(df_dic_temp)


            #f = open("C:\Users\jie.zhao@vgt.net\OneDrive\Dilution Analysis\DS_Dilution Analysis.csv", 'w')
            #outfile = "../dilution_events.csv"
            outfile = "dilution_events.csv"
            f=open(outfile, 'w')
            ##writer = csv.writer(f)
            ##writer.writerow(namesdf)
            output = str(namesdf)
            for row in df_list:
                output = output + '\n' + str(row)
                #print str(row) + "flerp"
                ##writer.writerow(row)
            output = output.replace('[', '')
            output = output.replace(']', '')
            output = output.replace('\'', '')
            f.write(output)
            #print output
            f.close()


print "Processing Complete: Results available in dilution_events.csv file"

raw_input("Press enter to exit")
