# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 10:59:03 2016

@author: jie.zhao
"""
import os
import csv
import numpy as np
import math

os.getcwd()
os.chdir('C:\python_projects\VGT_WAP_analysis')
#os.chdir('/Users/Jie/OneDrive/Grace/VGT_WAP_analysis')

f_s=open('Games_Cash_Seasonal_Index_normalized.csv')
csv_s=csv.reader(f_s)
datraw_s=[]
for row in csv_s:
    datraw_s.append(row) # now all the information is stored in
f_s.close()

date=[]
monthly_c=[]

datraw_s=datraw_s[1:]

for row in datraw_s:
    date.append(row[0])
    monthly_c.append(row[4])

#Index_s=date.index(20300713)

f=open('raw_WAP_LR_casino_Theo_monthly.csv')
csv_f=csv.reader(f)
datraw0=[]
datraw=[]
keyraw=[]
for row in csv_f:
    datraw0.append(row) # now all the information is stored in
f.close()
       
datraw0=[x for x in datraw0 if x[5] !='']
datraw0=[x for x in datraw0 if x[6] !='']

for row in datraw0[1:]:
    temp=row[1]
    temp=temp.replace('/','')
    temp='20'+temp[4:6]+temp[0:4]
    row_temp=[row[0]+'-'+temp,temp,row[2],row[3],row[4],row[5],row[6]]
    datraw.append(row_temp)
    keyraw.append(row_temp[0])

keylist=[]    
for key in keyraw:
    if key not in keylist:
        keylist.append(key)
        
jj=0
dat_customer_temp=[]
dat_customer0=[]
for dat_temp in datraw:
    if dat_temp[0]==keylist[jj]:
        dat_customer_temp.append(dat_temp)
    else: 
        jj=jj+1
        dat_customer0.append(dat_customer_temp)
        dat_customer_temp=[]
        dat_customer_temp.append(dat_temp)
dat_customer0.append(dat_customer_temp)

dat = [x for x in dat_customer0 if len(x)==4]

dat_f1=[]
dat_f2=[]

dat_f1_s=[]
dat_f2_s=[]

for dat_temp in dat:
    train=[]
    test=[]
    dat_temp0=dat_temp[0]
    date_temp=dat_temp0[1]
    date_index=date.index(date_temp)
    s_index=float(monthly_c[date_index])
    for temp in dat_temp:
        aa=temp[3]
        bb=temp[6]
        aa=aa.replace(',','')
        bb=bb.replace(',','')
        train.append(int(aa))
        test.append(int(bb))
    
    cc=dat_temp0[4]
    cc=cc.replace(',','')
    train.append(int(cc))
    dd=dat_temp0[5]
    dd=dd.replace(',','')
    train.append(int(dd))
    ee=dat_temp0[0]     
    dat_temp_f1=[ee[:-9],dat_temp0[1],train,test]
    test2=np.dot(train[:4],test)/sum(train[:4])
    dat_temp_f2=[ee[:-9],dat_temp0[1],train,test2]
    dat_f1.append(dat_temp_f1)
    dat_f2.append(dat_temp_f2)

    train_s=train[:5]+[train[5]*s_index]
    test_s=[x*s_index for x in test]
    dat_temp_f1_s=[ee[:-9],dat_temp0[1],train_s,test_s,s_index]
    test2_s=np.dot(train[:4],test_s)/sum(train[:4])
    dat_temp_f2_s=[ee[:-9],dat_temp0[1],train_s,test2_s,s_index]
    dat_f1_s.append(dat_temp_f1_s)
    dat_f2_s.append(dat_temp_f2_s)
    ##
    ##

# now let's start the epic of changing the current avg.theowin into pre.avg.theowin
# I. recording the unique customer, customerlist and theolist
customerkey=[]
customerlist=[]
avg_theo=[]
avg_theo_s=[]
for ii in range(0,len(dat_f1)):
    temp=dat_f1[ii]
    temp_s=dat_f1_s[ii]
    customerlist.append(temp[0])
    train=temp[2]
    train_s=temp_s[2]
    avg_theo.append(train[5])
    avg_theo_s.append(train_s[5])
    if temp[0] not in customerkey:
        customerkey.append(temp[0])
        
# II. find out the index of first occurence
index1=[]
for temp in customerkey:
    index1.append(customerlist.index(temp))
index1.reverse() # so that the poping from the end doesn't interfere the earlier indexes to be removed 

avg_theo_pre=avg_theo[:-1]
avg_theo_pre_s=avg_theo_s[:-1]
customerlist=customerlist[:-1]
for ii in index1[:-1]:
    avg_theo_pre.pop(ii-1)
    avg_theo_pre_s.pop(ii-1)
    customerlist.pop(ii-1)
#
dap_f1=dat_f1
dap_f2=dat_f2
dap_f1_s=dat_f1_s
dap_f2_s=dat_f2_s

for ii in index1:        
    dap_f1.pop(ii)
    dap_f2.pop(ii)
           
    dap_f1_s.pop(ii)
    dap_f2_s.pop(ii)
dat_f1=[]
dat_f2=[]
dat_f1_s=[]
dat_f2_s=[]
#        
for ii in range(0,len(dap_f1)):
    aa=[]
    bb=[]
    cc=[]
    dd=[]
    dap_f1_temp=dap_f1[ii]
    aa=dap_f1_temp[0]
    bb=dap_f1_temp[1]
    cc_temp=dap_f1_temp[2]
    dd=dap_f1_temp[3]
    cc=cc_temp[:5]+[avg_theo_pre[ii]]    
    dat_f1_temp=[aa,bb,cc,dd]
    dat_f1.append(dat_f1_temp)
    dap_f2_temp=dap_f2[ii]
    cc_temp=dap_f2_temp[2]
    dd=dap_f2_temp[3]
    cc=cc_temp[:5]+[avg_theo_pre[ii]]    
    dat_f2_temp=[aa,bb,cc,dd]
    dat_f2.append(dat_f2_temp)    
    
    dap_f1_temp_s=dap_f1_s[ii]
    cc_temp=dap_f1_temp_s[2]
    dd=dap_f1_temp_s[3]
    ee=dap_f1_temp_s[4]
    cc=cc_temp[:5]+[avg_theo_pre_s[ii]]
    dat_f1_temp_s=[aa,bb,cc,dd,ee]
    dat_f1_s.append(dat_f1_temp_s)
    dap_f2_temp_s=dap_f2_s[ii]
    cc_temp=dap_f2_temp_s[2]
    dd=dap_f2_temp_s[3]
    cc=cc_temp[:5]+[avg_theo_pre_s[ii]]    
    dat_f2_temp_s=[aa,bb,cc,dd,ee]
    dat_f2_s.append(dat_f2_temp_s)    
       
indexes=np.random.permutation(len(dat_f1))
temp=[]
for index in indexes :
    temp.append(dat_f1[index])
dat_f1=temp
temp=[]
for index in indexes :
    temp.append(dat_f2[index])
dat_f2=temp

temp=[]
for index in indexes :
    temp.append(dat_f1_s[index])
dat_f1_s=temp
temp=[]
for index in indexes :
    temp.append(dat_f2_s[index])
dat_f2_s=temp

dat_X1=[]
dat_X2=[]
dat_X1_s=[]
dat_X2_s=[]

dat_y1=[]
dat_y2=[]
dat_y1_s=[]
dat_y2_s=[]
s_indexf=[]

for xx in dat_f1:
    dat_X1.append(xx[2])
    dat_y1.append(xx[3])

for xx in dat_f2:
    dat_X2.append(xx[2])
    dat_y2.append(xx[3])    

for xx in dat_f1_s:
    dat_X1_s.append(xx[2])
    dat_y1_s.append(xx[3])

for xx in dat_f2_s:
    dat_X2_s.append(xx[2])
    dat_y2_s.append(xx[3])    
    s_indexf.append(xx[4])

X1_train = dat_X1[:-300]
X1_test = dat_X1[-300:]
y1_train = dat_y1[:-300]
y1_test = dat_y1[-300:]

X2_train = dat_X2[:-300]
X2_test = dat_X2[-300:]
y2_train = dat_y2[:-300]
y2_test = dat_y2[-300:]

X1_train_s = dat_X1_s[:-300]
X1_test_s = dat_X1_s[-300:]
y1_train_s = dat_y1_s[:-300]
y1_test_s = dat_y1_s[-300:]

X2_train_s = dat_X2_s[:-300]
X2_test_s = dat_X2_s[-300:]
y2_train_s = dat_y2_s[:-300]
y2_test_s = dat_y2_s[-300:]
s_indexf_test=s_indexf[-300:]

TW=dat_y2[-300:]
TW_c=[x[5] for x in dat_X1[-300:]]

from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from scipy import stats

fig, ax = plt.subplots()
ax.scatter(TW_c, TW)
ax.set_xlabel('TW_c')
ax.set_ylabel('TW')
plt.xlim((0,700))
plt.ylim((0,700))
plt.show()
rmsd0=math.sqrt(sum([math.pow((a-b),2) for a,b in zip(TW,TW_c)])/len(TW))
print 'rmsd0= ', rmsd0

#coefficient_of_dermination = r2_score(TW,TW_c)
#print 'r^2= ',coefficient_of_dermination
slope, intercept, r_value, p_value, std_err = stats.linregress(TW,TW_c)
#print 'r^2= ',coefficient_of_dermination
print 'r^2= ',r_value**2
correlation_coefficient=np.corrcoef(TW,TW_c)
print 'cc=', correlation_coefficient

clf = linear_model.LinearRegression()
clf.fit(X2_train,y2_train)
predicted=clf.predict(X2_test)
fig, ax = plt.subplots()
ax.scatter(y2_test, predicted)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.xlim((0,700))
plt.ylim((0,700))
plt.show()
rmsd1=math.sqrt(sum([math.pow((a-b),2) for a,b in zip(predicted,y2_test)])/len(predicted))
print 'rmsd1= ', rmsd1
slope, intercept, r_value, p_value, std_err = stats.linregress(predicted,y2_test)
#print 'r^2= ',coefficient_of_dermination
print 'r^2= ',r_value**2
correlation_coefficient=np.corrcoef(predicted,y2_test)
print 'cc=', correlation_coefficient
print 'coefficients', clf.coef_

clf = linear_model.LinearRegression()
poly = PolynomialFeatures(degree=2)
X2_trainf = poly.fit_transform(X2_train)
X2_testf = poly.fit_transform(X2_test)
clf.fit(X2_trainf, y2_train)
predicted=clf.predict(X2_testf)
fig, ax = plt.subplots()
ax.scatter(y2_test, predicted)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.xlim((0,700))
plt.ylim((0,700))
plt.show()
rmsd2=math.sqrt(sum([math.pow((a-b),2) for a,b in zip(predicted,y2_test)])/len(predicted))
print 'rmsd2= ', rmsd2
slope, intercept, r_value, p_value, std_err = stats.linregress(predicted,y2_test)
#print 'r^2= ',coefficient_of_dermination
print 'r^2= ',r_value**2
correlation_coefficient=np.corrcoef(predicted,y2_test)
print 'cc=', correlation_coefficient
print 'coefficients', clf.coef_


s_kk=np.array([1/x for x in s_indexf_test])
clf = linear_model.LinearRegression()
clf.fit(X2_train_s,y2_train_s)
predicted=clf.predict(X2_test_s)
fig, ax = plt.subplots()
ax.scatter(s_kk*np.array(y2_test_s), s_kk*np.array(predicted))
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.xlim((0,700))
plt.ylim((0,700))
plt.show()
rmsd3=math.sqrt(sum([math.pow((a-b),2) for a,b in zip(s_kk*np.array(predicted),s_kk*np.array(y2_test_s))])/len(predicted))
print 'rmsd3= ', rmsd3
print 'coefficients', clf.coef_

clf = linear_model.LinearRegression()
poly = PolynomialFeatures(degree=2)
X2_trainf_s = poly.fit_transform(X2_train_s)
X2_testf_s = poly.fit_transform(X2_test_s)
clf.fit(X2_trainf_s, y2_train_s)
predicted=clf.predict(X2_testf_s)
fig, ax = plt.subplots()
ax.scatter(s_kk*np.array(y2_test_s), s_kk*np.array(predicted))
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.xlim((0,700))
plt.ylim((0,700))
plt.show()

rmsd4=math.sqrt(sum([math.pow((a-b),2) for a,b in zip(s_kk*np.array(predicted),s_kk*np.array(y2_test_s))])/len(predicted))
print 'rmsd4= ', rmsd4
print 'coefficients', clf.coef_
