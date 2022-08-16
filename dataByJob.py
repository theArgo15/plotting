import pandas as pd
from pathlib import Path

#new data with only max temps per job
jobsData = pd.read_csv('jobsData.csv', index_col='Job')
#create blank csv file
pd.DataFrame(list()).to_csv('dataByJob.csv')
for row in jobsData.index:
    #find the information on all jobs
    print(jobsData.loc[row,'Path'])

    job = jobsData.loc[row, 'Path']
    filePath = Path(job)
    squareData = pd.read_csv(filePath/'squareData.csv')
    dataByJob = pd.read_csv('dataByJob.csv')

    #create lists for each attribute we want to create
    columnlist = []
    loggerNameList =[]
    loggerAttributeList = []
    for column in squareData.columns:
        if 'Temp' in column or 'Humidity' in column:
            columnlist.append(column)
    temporaryMax = squareData[columnlist].max()
    temporaryAverage = squareData[columnlist].mean()
    #some real nonsense to get column names right
    for logger in temporaryMax.index:
        if 'Temp' in logger:
            loggerNameList.append(logger.split('Temp')[0])
            loggerAttributeList.append('Temp')
        elif 'Humidity' in logger:
            loggerNameList.append(logger.split(('Humidity'))[0])
            loggerAttributeList.append('Humidity')

    #create dataframe with column information
    newJobData = pd.DataFrame(
        {'LoggerName':loggerNameList,
        'AttributeType' : loggerAttributeList,
        'AverageValue': temporaryAverage.values,
        'MaxValue': temporaryMax.values,
        'Job':[row]*len(loggerAttributeList)})

    dataByJob = pd.concat([dataByJob,newJobData])
    dataByJob.to_csv('dataByJob.csv',index=False)

#add job description as a column
#I hate that I did this in a loop. I'm reasonably certain there is a way to apply a lookup table or something to do this way better
dataByJob = pd.read_csv('dataByJob.csv')
jobsData = pd.read_csv('jobsData.csv', index_col='Job')
descriptionList = []
for row in dataByJob.index:
    jobNumber=dataByJob.loc[row,'Job']
    descriptionList.append(jobsData.loc[jobNumber,'Description'])
newJobData = pd.DataFrame(
        {'Description':descriptionList})
dataByJob = pd.concat([dataByJob, newJobData], axis=1)
dataByJob.to_csv('dataByJob.csv',index=False)