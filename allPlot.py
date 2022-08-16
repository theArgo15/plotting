from ast import Not
from lib2to3.pgen2.pgen import DFAState
from logging import raiseExceptions
import re
from sqlite3 import Time
from tkinter.tix import Tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import referenceVariable

def attributePlotter(df, attribute):
    fig, ax = plt.subplots()
    colormap = plt.cm.nipy_spectral
    colors = [colormap(i) for i in np.linspace(0, 1,22)]
    ax.set_prop_cycle('color', colors)
    for column in df.columns:
        if attribute in column:
            if 'Logger' in column:
                #loggers greater than 9 are using logger 1 time
                if len(column) == 11:
                    loggerNumber = column[6]
                elif len(column) == 12:
                    loggerNumber = column[6:8]
                else:
                    raise Exception("logger number out of bounds")
                ax.plot(f'Logger{loggerNumber}Time', column, data=df, label=column)
                print(loggerNumber)
            else:
                ax.plot('Time', column, data=df, label=column)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(f'{attribute} ($^\circ$C) or (%)')
    ax.set_title('Control')
    ax.legend()



def splitAttributePlotter(df, attribute):
    #6 total graphs: 4 engines, EP bay, SVP tracked stuff
    fig, axs = plt.subplots(3,2, sharex=True, sharey=True)
    jobFinishTime = df['Time'].max()
    for i in range(4):
        axs[0, 0].plot(f'Logger{i+1}Time', f'Logger{i+1}{attribute}', data=df, label = referenceVariable.LocationDescriptions.loc[f'Logger{i+1}', 'Location Position'])
        axs[0, 1].plot(f'Logger{i+5}Time', f'Logger{i+5}{attribute}', data=df, label = referenceVariable.LocationDescriptions.loc[f'Logger{i+5}', 'Location Position'])
        axs[1, 0].plot(f'Logger{i+9}Time', f'Logger{i+9}{attribute}', data=df, label = referenceVariable.LocationDescriptions.loc[f'Logger{i+9}', 'Location Position'])
        axs[1, 1].plot(f'Logger{i+13}Time', f'Logger{i+13}{attribute}', data=df, label = referenceVariable.LocationDescriptions.loc[f'Logger{i+13}', 'Location Position'])
    for i in range(3):
        try:
            axs[2, 0].plot(f'Logger{i+17}Time', f'Logger{i+17}{attribute}', data=df, label = referenceVariable.LocationDescriptions.loc[f'Logger{i+17}', 'Location Position'])
        except:
            raise Warning('Logger 19 not found')
    #some terrible logic for getting ECS supply, return, and EP attribute 
    for column in df.columns:
        if attribute in column:
            if 'Logger' in column:
                pass
            elif 'room' in column:
                axs[2,0].plot('roomTime', column, data = df, label=column)
            else:
                axs[2,1].plot('Time', column, data=df, label=column)

    plotTitles = ['Engine 1', 'Engine 2', 'Engine 3', 'Engine 4', 'Misc Locations', 'SVP Tracked Data']
    for i, ax in enumerate(axs.reshape(-1)):
        ax.axvline(x=jobFinishTime)
        ax.set_title(plotTitles[i])
        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(attribute + referenceVariable.attributeUnits[attribute])
    return jobFinishTime

def PositionSplitAttributePlotter(df, attribute):
    fig, axs = plt.subplots(2,2, sharex=True, sharey=True)
    jobFinishTime = df['Time'].max()
    every4 =[1,5,7,11]
    for LoggerLabel in every4:
        axs[0, 0].plot(f'Logger{LoggerLabel}Time', f'Logger{LoggerLabel}{attribute}', data=df, label = f'Logger{LoggerLabel}')
        axs[0, 1].plot(f'Logger{LoggerLabel+1}Time', f'Logger{LoggerLabel+1}{attribute}', data=df, label = f'Logger{LoggerLabel+1}')
        axs[1, 0].plot(f'Logger{LoggerLabel+2}Time', f'Logger{LoggerLabel+2}{attribute}', data=df, label = f'Logger{LoggerLabel+2}')
        axs[1, 1].plot(f'Logger{LoggerLabel+3}Time', f'Logger{LoggerLabel+3}{attribute}', data=df, label = f'Logger{LoggerLabel+3}')

    for i, ax in enumerate(axs.reshape(-1)):
        ax.axvline(x=jobFinishTime)
        ax.set_title(f'Position {i+1}')
        ax.legend()
    return jobFinishTime

if __name__ == "__main__":
    jobsData = pd.read_csv('jobsData.csv', index_col='Job')
    #input
    job = 1660244076
    #this is either Temp or Humidity
    plotAttribute ='Temp'
    jobDate = jobsData.loc[job, 'Date']
    jobDescription = jobsData.loc[job, 'Description']
    plotTitle = f'{jobDate} Data ({jobDescription})'

    job = jobsData.loc[job, 'Path']
    job = Path(job)
    dataLocation = pd.read_csv(job/'syncedData.csv')
    

    jobFinishTime = splitAttributePlotter(dataLocation, plotAttribute)
    #plt.xlim([0,jobFinishTime+900])
    #this x limit is 900 seconds after the end of the FAT build
    plt.xlim([0,12195.52+900])
    if plotAttribute == 'Temp':
        plt.ylim([20,27])
    elif plotAttribute == 'Humidity':
        #Limits for RH
        plt.ylim([20,50])
    else:
        print('Plot attribute not recognized')
    plt.suptitle(plotTitle)
    plt.show(block=True)
    #plt.savefig(Path(r"C:\Users\TonyWitt\OneDrive - Evolve\Pictures")/'test')