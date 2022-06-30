import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

#start time in unix timestamp is the first part of the title of the xl sheet
jobStartTime = 1656084383
#import job data into dataframe
internalData = pd.read_excel(f'{str(jobStartTime)}_appLogs.xlsx')
#import all the logger data into dataframe
#with 18 temp loggers, this might be a loop of some sort
filePath = Path(r'C:\Users\TonyWitt\OneDrive - Evolve\Documents\Flir Logs')
externalData = pd.read_csv(filePath/'Logger1.xls', skiprows=7, sep='\t', parse_dates=[['DATE','TIME']])


#Create and save dataframe of data we care about from logger and internal data
svp2Job = internalData.loc[:,('Time','EPTemp', 'EPHumidity','ECSReturnTemp', 'ECSReturnHumidity','ECSSupplyTemp','ECSSupplyHumidity')]
# #get a column of unix time
# svp2Job['ECSSupplyTemp'] = externalData['ECSSupplyTemp']
svp2Job['TimeInEpoc'] = svp2Job['Time'] + jobStartTime
svp2Job['SVPTime'] = pd.to_datetime(svp2Job['TimeInEpoc'], unit='s') 
# Add column for each logger time, logger temp, logger RH

### Drop the old table.
#svp2Job.drop('Time', axis = 1, inplace = True)
#write out new table
svp2Job.to_csv('newNewData.csv', index = False)
pass