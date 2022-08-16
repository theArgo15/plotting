import pandas as pd
from pathlib import Path

def squareTheData(filePath):
    syncedData = pd.read_csv(filePath/'syncedData.csv')
    squareData = syncedData[['Time','EPTemp', 'EPHumidity','ECSReturnTemp', 'ECSReturnHumidity','ECSSupplyTemp','ECSSupplyHumidity']]
    #get rid of extra space
    squareData = squareData[squareData['Time'].notnull()]
    jobEndTime = squareData['Time'].max()
    #need loop for all loggers
    for i in range(19):
        #create filter to get only job data for loggers
        timeFilter = (syncedData[f'Logger{i+1}Time'] > 0) & (syncedData[f'Logger{i+1}Time'] < jobEndTime)
        #apply filter to the 3 columns assc with the logger
        filteredLoggerData = syncedData.loc[timeFilter,[f'Logger{i+1}Time',f'Logger{i+1}Temp',f'Logger{i+1}Humidity']].reset_index()
        squareData = pd.concat([squareData, filteredLoggerData],axis=1)
    #new filter for room data
    timeFilter = (syncedData['roomTime'] > 0) & (syncedData['roomTime'] < jobEndTime)
    #apply filter to the 3 columns assc with room reference
    filteredRoomData = syncedData.loc[timeFilter,['roomTime','roomTemp','roomHumidity']].reset_index()
    squareData = pd.concat([squareData, filteredRoomData],axis=1)
    squareData.to_csv(filePath/'squareData.csv', index = False)

if __name__ == "__main__":
    jobsData = pd.read_csv('jobsData.csv', index_col='Job')
    #input
    job = 1660319120

    job = jobsData.loc[job, 'Path']
    job = Path(job)

    squareTheData(job)