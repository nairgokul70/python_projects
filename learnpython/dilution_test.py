"""
Created on Thu Jan 28 20:33:35 2016 by jie.zhao
Revised on Tues Mar 1 12:52:33 2016 by ian.burchett
Refactored on Tues Oct 4, 2016 by Sonya Feinberg
Modified to include Denom and Paytable Series parameters  on Tues. Oct 25, 2016 by Sonya Feinberg
@author: jie.zhao, ian.burchett
"""

import os
import csv
from os import path
import jpype

####################### Functions ############################################################

## Build a where clause from input lists.
def setWhereClause(sList, dList):

    sql_Serieswhere="paytableSeries in ('"
    for i in range(len(sList)):
        if i == "*":
          sql_Serieswhere = ""
          break
        ## if first index element skip adding semicolon
        if (i == 0):
          sql_Serieswhere = sql_Serieswhere + str(sList[i]).upper()
        else:
          sql_Serieswhere= sql_Serieswhere + "','" + str(sList[i])
    sql_Serieswhere = sql_Serieswhere + "')"

    sql_Denomwhere="denom in ("
    for i in range(len(dList)):
        denomI = str(dList[i])

        if i == "*":
          sql_Denomwhere = ""
          break

        ## check for formatting
        if (denomI.isdigit()):
            denomI = "'$"+denomI.zfill(1)+".00'"
        else:
            if denomI.count(".") == 0:
              denomI = denomI+".00"
            if denomI.count("$") == 0:
              denomI = "$"+denomI

        ## if first index element skip adding semicolon
        if (i == 0):
          sql_Denomwhere = sql_Denomwhere + denomI
        else:
          sql_Denomwhere= sql_Denomwhere  + "," + denomI
    sql_Denomwhere = sql_Denomwhere + ")"

    if (sql_Serieswhere != ""):
      sql_where = 'where ' + sql_Serieswhere
      if (sql_Denomwhere != ""):
        sql_where = sql_where + ' and ' + sql_Denomwhere

    return sql_where;


##Function to write query results to an output file
def writeQueryResultsToFile( outputfilename ):
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
    outfile = open(outputfilename, 'w')
    outfile.write(output)
    outfile.close()
    return;


def readQueryResultsFromFile( inputFilename ):
  xfile = inputFilename
  f=open(xfile)
  csv_f=csv.reader(f)
  datraw=[]
  for row in csv_f:
    datraw.append(row)

  return datraw;


def prepareDenomSeriesData(denomSeriesRaw):
    firstDenomSeriesRaw=denomSeriesRaw[1]

    prevCustomerNumber = firstDenomSeriesRaw[customerNumberIdx]
    prevCustomerName   = firstDenomSeriesRaw[customerNameIdx]
    prevYearMonth      = firstDenomSeriesRaw[yearIdx] + '-' + firstDenomSeriesRaw[monthIdx]
    sumBeginFootprint = int(firstDenomSeriesRaw[beginFootprintIdx])
    sumDeltaPTCount   = int(firstDenomSeriesRaw[deltaPtcountIdx])
    sumGamesPlayed    = int(firstDenomSeriesRaw[gamesPlayedIdx])
    sumActualWin      = float(firstDenomSeriesRaw[actualWinIdx])
    sumTheoWin        = float(firstDenomSeriesRaw[theoWinIdx])
    sumMachineDays    = int(firstDenomSeriesRaw[machineDaysIdx])
    sumGamesPlayedAdj = float(firstDenomSeriesRaw[gamesPlayedAdjIdx])
    sumActualWinAdj   = float(firstDenomSeriesRaw[actualWinAdjIdx])
    sumTheoWinAdj     = float(firstDenomSeriesRaw[theoWinAdjIdx])

    for i in denomSeriesRaw[1:]:
      if (i[yearIdx] + '-' + i[monthIdx]) == prevYearMonth:
        sumBeginFootprint = sumBeginFootprint + int(i[beginFootprintIdx])
        sumDeltaPTCount   = sumDeltaPTCount   + int(i[deltaPtcountIdx])
        sumGamesPlayed    = sumGamesPlayed    + int(i[gamesPlayedIdx])
        sumActualWin      = sumActualWin      + float(i[actualWinIdx])
        sumTheoWin        = sumTheoWin        + float(i[theoWinIdx])
        sumMachineDays    = sumMachineDays    + int(i[machineDaysIdx])
        sumGamesPlayedAdj = sumGamesPlayedAdj + float(i[gamesPlayedAdjIdx])
        sumActualWinAdj   = sumActualWinAdj   + float(i[actualWinAdjIdx])
        sumTheoWinAdj     = sumTheoWinAdj     + float(i[theoWinAdjIdx])
      else:
        #save now because you are at the end of a year-month grouping
        row_temp=[prevCustomerNumber,prevCustomerName,prevYearMonth, sumBeginFootprint,sumDeltaPTCount,sumGamesPlayed,sumActualWin,sumTheoWin,sumMachineDays,sumGamesPlayedAdj,sumActualWinAdj,sumTheoWinAdj]
        #store list of customers
        customerlistraw.append(prevCustomerNumber)
        #reset the values to the first occurance of year-month grouping
        prevCustomerNumber    = i[customerNumberIdx]
        prevCustomerName      = i[customerNameIdx]
        prevYearMonth         = i[yearIdx] + '-' + i[monthIdx]
        sumBeginFootprint    = int(i[beginFootprintIdx])
        sumDeltaPTCount   = int(i[deltaPtcountIdx])
        sumGamesPlayed    = int(i[gamesPlayedIdx])
        sumActualWin      = float(i[actualWinIdx])
        sumTheoWin        = float(i[theoWinIdx])
        sumMachineDays    = int(i[machineDaysIdx])
        sumGamesPlayedAdj = float(i[gamesPlayedAdjIdx])
        sumActualWinAdj   = float(i[actualWinAdjIdx])
        sumTheoWinAdj     = float(i[theoWinAdjIdx])
        dat.append(row_temp)
    return;



def prepareCustomerData(datraw):
  for i in datraw[1:]:
    row_temp=[i[customerNumberIdx],i[customerNameIdx],i[yearIdx]+'-'+i[monthIdx], i[beginFootprintIdx], i[deltaPtcountIdx], i[gamesPlayedIdx], i[actualWinIdx], i[theoWinIdx], i[machineDaysIdx], i[gamesPlayedAdjIdx], i[actualWinAdjIdx], i[theoWinAdjIdx]]
    dat.append(row_temp)
    customerlistraw.append(i[0])
  return;


def doSomethingWithCustomerList():
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
        #print(" Dat Temp: " + str(dat_temp))

        if jj<customer_n:
            if dat_temp[0]==customerlist[jj]:
                dat_customer_temp.append(dat_temp)
                #print(" Dat customer Temp: " + str(dat_customer_temp))

            else:
                jj=jj+1
                dat_customer0.append(dat_customer_temp)
                #print(" Else dat customer0: " + str(dat_customer0) )
                dat_customer_temp=[]
                dat_customer_temp.append(dat_temp)

    dat_customer0.append(dat_customer_temp)
    dat_customer = [x for x in dat_customer0 if x != []]

    return dat_customer;


## This function takes the delta pt count vector and sets up three vectors used in the aggregation method
# capture the vectors, one for storing the beginning index of events based on DeltaPtCount vector
# one that stores the sums (DeltaPTCount) for the events, matching the index vector on size
# one for storing the ending index of events based on DeltaPtCount vector
# note: first month will not be included in sum of counts(i>0)
def setEventVectors(deltaptcount_vec, event_bindex, event_eindex, event_sum):
    countContinuousZeros = 1
    valueSum = 0
    lengthBindex = 0
    for i,value in enumerate(deltaptcount_vec):
      #print("Appending: " + " i: " + str(i) + " value: " + str(value) + " valueSum: " + str(valueSum) + " Zeros: " + str(countContinuousZeros) + " Bindex LEN: " + str(len(event_bindex)))

      if value == 0:
        countContinuousZeros = countContinuousZeros + 1

      if value!=0 and countContinuousZeros >1:
        event_bindex.append(i)
        lengthBindex = len(event_bindex)

        if lengthBindex >= 2:
          event_sum.append(valueSum)

        valueSum = 0
        countContinuousZeros = 0

      elif value!=0:
        countContinuousZeros = 0

      if value==0 and countContinuousZeros == 2 and lengthBindex >= 1:
        event_eindex.append(i-2)

      if i>0:
        valueSum = valueSum + value

    event_sum.append(valueSum)
    ## may be missing last ending index month so test for this and add last index.
    if len(event_eindex) < len(event_bindex):
       event_eindex.append(len(deltaptcount_vec) - 1)
    #print("Event_Bindex: " + str(event_bindex))
    #print("Event_Sum: " + str(event_sum))
    #print("Event_Eindex: " + str(event_eindex))
    return;



## This function uses the EventVectors and the parameter thesholds to aggregate the months surrounding an event.
## And builds the df_list used in output
def aggregatePriorPostMonths(df_list, cLevel, deltaptcount_vec, event_bindex, event_eindex, event_sum, dic_customer, time_vec, beginEGM_vec, gamesplayed_vec, adjgamesplayed_vec, theowin_vec, adjtheowin_vec, actualwin_vec, adjactualwin_vec, machinedays_vec):

  threshold = threshN
  if cLevel == "TRUE":
    threshhold = 1

  ##Only the Casino Level report will use the EGM threshold setting
  df_dic_temp={}

  ## process all values within the threshold parameter and any where there are enough months going back and forward for aggregation.
  if len(event_bindex) > 0:
    for i, value in enumerate(event_sum):
      if value >= threshold and event_bindex[i] - preN > 0 and event_eindex[i] + postN + 1 < len(deltaptcount_vec):
         #print(str(dic_customer[names[0]]) + " Event: " + str(event_bindex[i]) + " " + str(event_eindex[i]) )
         df_dic_temp['customernumber']=dic_customer[names[0]]
         df_dic_temp['customername']=dic_customer[names[1]]
         #print("Time vec: " + str(dic_customer[names[2]]) + " b: " + str(event_bindex[i] - preN) + " e: " + str(event_eindex[i] + postN ))
         df_dic_temp['starttime']=time_vec[ event_bindex[i] ]
         df_dic_temp['endtime']=time_vec[ event_eindex[i] ]
         df_dic_temp['beginfootprint']=beginEGM_vec[ event_bindex[i] - 1 ]
         df_dic_temp['afterfootprint']=beginEGM_vec[ event_eindex[i] + 1 ]
         df_dic_temp['deltaptcount']=event_sum[i]
         df_dic_temp['%EGMchange']=float(df_dic_temp['deltaptcount'])/float(df_dic_temp['beginfootprint'])

         df_dic_temp['preUtilization']=sum(gamesplayed_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])/14400.0
         df_dic_temp['adjpreUtilization']=sum(adjgamesplayed_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])/14400.0
         df_dic_temp['postUtilization']=sum(gamesplayed_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/14400.0
         df_dic_temp['adjpostUtilization']=sum(adjgamesplayed_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/14400.0

         #print(" Pre Event Range: " + str(event_bindex[i] - preN) + " to " + str(event_bindex[i]) )
         #print(" Post Event Range: " + str(event_eindex[i] +1 ) + " to " + str(event_eindex[i] + postN +1 ) )
         df_dic_temp['preTheoWPUPD']=sum(theowin_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])
         df_dic_temp['adjpreTheoWPUPD']=sum(adjtheowin_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])
         df_dic_temp['postTheoWPUPD']=sum(theowin_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])
         df_dic_temp['adjpostTheoWPUPD']=sum(adjtheowin_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])
         #print(" Pre TheoWin: " + str(sum(theowin_vec[ event_bindex[i] - preN:event_bindex[i] ])) + " MD " + str(sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])) )
         #print(" Post TheoWin: " + str(sum(theowin_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])) + " MD " + str(sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])) )
         df_dic_temp['preActualWPUPD']=sum(actualwin_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])
         df_dic_temp['adjpreActualWPUPD']=sum(adjactualwin_vec[ event_bindex[i] - preN:event_bindex[i] ])/sum(machinedays_vec[ event_bindex[i] - preN:event_bindex[i] ])
         df_dic_temp['postActualWPUPD']=sum(actualwin_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])
         df_dic_temp['adjpostActualWPUPD']=sum(adjactualwin_vec[ event_eindex[i] +1:event_eindex[i] + postN +1 ])/sum(machinedays_vec[ event_eindex[i] +1:event_eindex[i] + postN +1])

         ##Test for zero divide
         if df_dic_temp['preTheoWPUPD'] > 0:
           df_dic_temp['%TheoWchange']=(df_dic_temp['postTheoWPUPD']-df_dic_temp['preTheoWPUPD'])/df_dic_temp['preTheoWPUPD']
           df_dic_temp['%ActualWchange']=(df_dic_temp['postActualWPUPD']-df_dic_temp['preActualWPUPD'])/df_dic_temp['preActualWPUPD']
           df_dic_temp['DFtheo']= df_dic_temp['%TheoWchange']/df_dic_temp['%EGMchange']
           df_dic_temp['DFactual']= df_dic_temp['%ActualWchange']/df_dic_temp['%EGMchange']
           df_dic_temp['adj%TheoWchange']=(df_dic_temp['adjpostTheoWPUPD']-df_dic_temp['adjpreTheoWPUPD'])/df_dic_temp['adjpreTheoWPUPD']
           df_dic_temp['adj%ActualWchange']=(df_dic_temp['adjpostActualWPUPD']-df_dic_temp['adjpreActualWPUPD'])/df_dic_temp['adjpreActualWPUPD']
           df_dic_temp['adjDFtheo']= df_dic_temp['adj%TheoWchange']/df_dic_temp['%EGMchange']
           df_dic_temp['adjDFactual']= df_dic_temp['adj%ActualWchange']/df_dic_temp['%EGMchange']
         else:
           df_dic_temp['%TheoWchange']=0
           df_dic_temp['%ActualWchange']=0
           df_dic_temp['DFtheo']= 0
           df_dic_temp['DFactual']= 0
           df_dic_temp['adj%TheoWchange']=0
           df_dic_temp['adj%ActualWchange']=0
           df_dic_temp['adjDFtheo']=0
           df_dic_temp['adjDFactual']=0

         df_temp=[]
         for j in namesdf:
           df_temp.append(df_dic_temp[j])

         df_list.append(df_temp)

  return df_list;


def processCustomerList(df_list, cLevel):

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


    #print("DeltaPTCount_Vec: " + str(deltaptcount_vec))
    #print("time vec: " + str(dic_customer[names[2]]))
    #print("Begin EGM vec " + str(dic_customer[names[3]]))

    event_bindex=[]
    event_eindex=[]
    event_sum=[]


    ##Call to function to set the three vectors required using deltaptcount_vec
    setEventVectors(deltaptcount_vec, event_bindex, event_eindex, event_sum)

    ##Function call to aggregate the data Prior and Past months and build the df_list vector for output.
    df_list = aggregatePriorPostMonths(df_list, cLevel, deltaptcount_vec, event_bindex, event_eindex, event_sum, dic_customer, time_vec, beginEGM_vec, gamesplayed_vec, adjgamesplayed_vec, theowin_vec, adjtheowin_vec, actualwin_vec, adjactualwin_vec, machinedays_vec)

  return df_list;



##Function to write the header (namesdf) and the output vector (df_List) to a file
def writeDFList( df_list, outputFilename ):

  outfile = outputFilename
  f=open(outfile, 'w')
  ##writer = csv.writer(f)
  ##writer.writerow(namesdf)
  output = str(namesdf)
  for row in df_list:
    output = output + '\n' + str(row)
    ##print str(row) + "flerp"
    ##writer.writerow(row)
  output = output.replace('[', '')
  output = output.replace(']', '')
  output = output.replace('\'', '')
  f.write(output)
  #print output
  f.close()
  return;


#############################################################################################################################################

rawByCustomerFilename = "raw_dilution.csv"
rawByCustomerDenomSeriesFilename = "raw_denomSeriesDilution.csv"


denomList=[]
seriesList=[]


try:
  print("\n \n Note:  Calculations for the before and after aggregated measures for each event will not ")
  print("        include the month or months involved in the change event.")
  print("        Change events may span months and may include a month of no change if immediately followed ")
  print("        by a month of increase-decrease in EGM count. ")
  print("\n        Change events at the Denom-Paytable Series level do not have a EGM treshold setting and ")
  print("        report all increases. \n\n")


  threshN = input('Please input number of machines increase required to initiate a dilution event at teh Casino level (i.e. 25): ')
  preN = input('Please input number of months BEFORE a dilution event, to analyze (i.e. 12): ')
  postN = input('Please input number of months AFTER a dilution event, to analyze (i.e. 12): ')

  print("\nDenoms example options ('*' = all) :         [.25, 1, 2, 5] or [10] or  ['*'] ")
  print("Paytable Series example options ('*' = all) :  ['M1', 'M4', 'M37WAP', 'M38WAP'] or ['M12'] or ['*'] ")

  denomList = input('\nPlease enter a comma seperated list of denoms:  ')
  seriesList = input('Please enter a comma seperated list of paytable series: ')
except:
   print("\n\n********Please enter a VALID input and make sure to use Square Brackets ******************")
   print("\n Denom examples:   ['*'] or  [.25, 1, 2, 5, 10] ")
   print("\n Paytable Series example: ['*'] or ['M1','M4'] ")
   raise SystemExit, 0

print "Pulling raw data from Discovery Zone on Vertica, please wait..."

#load data from Vertica
from jaydebeapi import connect
connection = connect('com.vertica.jdbc.Driver',['jdbc:vertica://vertica01/vgt_edw','TB_temp','tbtemp'],'C:/Python27/vertica-jdbc.jar')
cur = connection.cursor()




##Denom Paytable Series Level query
sql_select=' SELECT customernumber, customername, denom, paytableseries, year, month, beginfootprint, deltaptcount, trainset, gamesPlayed, ActualWin, TheoWin, MachineDays, GamesPlayedAdj, ActualWinAdj, TheoWinAdj '
sql_from=' FROM dz.vw_DilutionDenomSeries '
sql_group_order=' ORDER BY customernumber, year, month'
sql_where = setWhereClause(seriesList, denomList)

query=sql_select+sql_from+sql_where+sql_group_order

print(" Query: " + str(query))
cur.execute(query)

results = cur.fetchall()

#Call to method that writes query to file
writeQueryResultsToFile( rawByCustomerDenomSeriesFilename )

print "Processing data..."


#Call to method that reads the query results in a file, returning a list
denomSeriesRaw = readQueryResultsFromFile( rawByCustomerDenomSeriesFilename )




#create new dat that contains only the essential variables
namesraw=denomSeriesRaw[0]

names=[namesraw[0]   ,namesraw[1],'year-month',namesraw[4]   ,namesraw[5] ,namesraw[7],namesraw[8],namesraw[9],namesraw[10],namesraw[11]  ,namesraw[12],namesraw[13]]
###### CustomerNumber,CustomerName,Year-Month ,BeginFootprint,DeltaPTCount,GamesPlayed,ActualWin  ,TheoWin    ,MachineDays ,GamesPlayedAdj,ActualWinAdj,TheoWinAdj    ##############################

namesdf=['customernumber','customername','starttime','endtime','beginfootprint','afterfootprint','deltaptcount','%EGMchange'
     ,'preUtilization','adjpreUtilization','postUtilization','adjpostUtilization','preTheoWPUPD','adjpreTheoWPUPD'
     ,'postTheoWPUPD','adjpostTheoWPUPD','preActualWPUPD','adjpreActualWPUPD','postActualWPUPD','adjpostActualWPUPD'
     ,'%TheoWchange','adj%TheoWchange','%ActualWchange','adj%ActualWchange','DFtheo','adjDFtheo','DFactual','adjDFactual']


############### Process DenomSeries data #######################################################################
customerNumberIdx = 0
customerNameIdx   = 1
yearIdx           = 4
monthIdx          = 5
beginFootprintIdx = 6
deltaPtcountIdx   = 7
gamesPlayedIdx    = 9
actualWinIdx      = 10
theoWinIdx        = 11
machineDaysIdx    = 12
gamesPlayedAdjIdx = 13
actualWinAdjIdx   = 14
theoWinAdjIdx     = 15

dat=[]
customerlistraw=[]




## method call to aggregate/group by denom and series to the customer, year, month level
prepareDenomSeriesData(denomSeriesRaw)





datn=len(dat)


##print(" Dat: " + str(dat))
## Call function to do something that returns the customer list used for looping in processCustomerList()
dat_customer = doSomethingWithCustomerList()




customer_dic=[] # the list that stores of dic_customer{} that stores all info for each customer
df_dic=[]
df_list=[]

## Method that loop through distinct customers to process and build final df_list
df_list = processCustomerList(df_list, cLevel = "TRUE")




##Function call to write the header (namesdf) and the output vector (df_List) to a file
writeDFList(df_list, outputFilename = "dilutionDenomSeries_events.csv")



##################################################################################################################

print "Processing Complete: Results available in dilution_events.csv and dilutionDenomSeries_events.csv file"

raw_input("Press enter to exit")



