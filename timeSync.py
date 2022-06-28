import numpy as np
import pandas as pd
from datetime import datetime

#start time in unix timestamp is the first part of the title of the xl sheet
jobStartTime = 1656084383
#import job data into dataframe
internalData = pd.read_excel('1656084383_appLogs.xlsx')
#import all the logger data into dataframe
#with 18 temp loggers, this might be a loop of some sort
externalData = pd.read_csv('newData.csv')
#Create and save dataframe of data we care about from logger and internal data
svp2Job = internalData.loc[:,('Time','EPTemp', 'EPHumidity','ECSReturnTemp', 'ECSReturnHumidity','ECSSupplyTemp','ECSSupplyHumidity')]
#get a column of unix time
svp2Job['ECSSupplyTemp'] = externalData['ECSSupplyTemp']
svp2Job['TimeInEpoc'] = svp2Job['Time'] + jobStartTime
svp2Job['TimeInGMT'] = pd.to_datetime(svp2Job['TimeInEpoc'], unit='s') 
### Drop the old table.
#svp2Job.drop('Time', axis = 1, inplace = True)
#write out new table
svp2Job.to_csv('newNewData.csv', index = False)
pass