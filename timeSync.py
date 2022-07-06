import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

#start time in unix timestamp is the first part of the title of the xl sheet
jobStartTime = 1656605942
#File path will need to be updated for each folder of data
filePath = Path(r'C:\Users\TonyWitt\OneDrive - Evolve\Documents\Flir Logs\30Jun')
#import job data into dataframe
internalData = pd.read_excel(filePath/f'{str(jobStartTime)}_appLogs.xlsx')

#Create and save dataframe of data we care about from logger and internal data
SVP2Job = pd.DataFrame(index=range(16000),columns=range(1))
svp2Job = pd.concat([SVP2Job, internalData.loc[:,('Time','EPTemp', 'EPHumidity','ECSReturnTemp', 'ECSReturnHumidity','ECSSupplyTemp','ECSSupplyHumidity')]],axis=1)
# #get a column of unix time
svp2Job['TimeInEpoc'] = svp2Job['Time'] + jobStartTime
svp2Job['SVPTime'] = pd.to_datetime(svp2Job['TimeInEpoc'], unit='s') 
#import all the logger data into dataframe
#with 18 temp loggers, this might be a loop of some sort

for i in range(18):
    # Add column for each logger time, logger temp, logger RH
    # Logger time starts as datetime. Convert into epoch time by subtracting jan 1 1970 and displaying total seconds, then subtract jobStartTime to get synced time
    externalData = pd.read_csv(filePath/f'Logger{i+1}.xls', skiprows=7, sep='\t', parse_dates=[['DATE','TIME']])
    svp2Job[f'Logger{i+1}DateTime'] = externalData['DATE_TIME'].dt.tz_localize(tz='US/Central')
    svp2Job[f'Logger{i+1}Time'] =  svp2Job[f'Logger{i+1}DateTime'].astype('int64')//1e9 - jobStartTime
    svp2Job[f'Logger{i+1}Temp'] = externalData['TEMPERATURE']
    svp2Job[f'Logger{i+1}Humidity'] = externalData['RELATIVE-HUMIDITY']
### Drop the old table.
#svp2Job.drop('Time', axis = 1, inplace = True)
#write out new table
svp2Job.to_csv(filePath/'syncedData.csv', index = False)
pass