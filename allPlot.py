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

def featurePlotter(df, feature):
    fig, ax = plt.subplots()
    colormap = plt.cm.nipy_spectral
    colors = [colormap(i) for i in np.linspace(0, 1,22)]
    ax.set_prop_cycle('color', colors)
    for column in df.columns:
        if feature in column:
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
    ax.set_ylabel(f'{feature} ($^\circ$C) or (%)')
    ax.set_title('Control')
    ax.legend()



def splitFeaturePlotter(df, feature):
    #6 total graphs: 4 engines, EP bay, SVP tracked stuff
    fig, axs = plt.subplots(3,2, sharex=True, sharey=True)
    jobFinishTime = df['Time'].max()
    for i in range(4):
        axs[0, 0].plot(f'Logger{i+1}Time', f'Logger{i+1}{feature}', data=df, label = f'Logger{i+1}')
        axs[0, 1].plot(f'Logger{i+5}Time', f'Logger{i+5}{feature}', data=df, label = f'Logger{i+5}')
        axs[1, 0].plot(f'Logger{i+9}Time', f'Logger{i+9}{feature}', data=df, label = f'Logger{i+9}')
        axs[1, 1].plot(f'Logger{i+13}Time', f'Logger{i+13}{feature}', data=df, label = f'Logger{i+13}')
    for i in range(3):
        try:
            axs[2, 0].plot(f'Logger{i+17}Time', f'Logger{i+17}{feature}', data=df, label = f'Logger{i+17}')
        except:
            raise Warning('Logger 19 not found')
    #some terrible logic for getting ECS supply, return, and EP feature 
    for column in df.columns:
        if feature in column:
            if 'Logger' in column:
                pass
            else:
                axs[2,1].plot('Time', column, data=df, label=column)

    plotTitles = ['Engine 1', 'Engine 2', 'Engine 3', 'Engine 4', 'Electronics Bay', 'SVP Tracked Data']
    featureUnits = {'Temp': '($^\circ$C)', 'Humidity': '(%)'}
    for i, ax in enumerate(axs.reshape(-1)):
        ax.axvline(x=jobFinishTime)
        ax.set_title(plotTitles[i])
        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(feature + featureUnits[feature])
    return jobFinishTime

def PositionSplitFeaturePlotter(df, feature):
    fig, axs = plt.subplots(2,2, sharex=True, sharey=True)
    jobFinishTime = df['Time'].max()
    every4 =[1,5,7,11]
    for LoggerLabel in every4:
        axs[0, 0].plot(f'Logger{LoggerLabel}Time', f'Logger{LoggerLabel}{feature}', data=df, label = f'Logger{LoggerLabel}')
        axs[0, 1].plot(f'Logger{LoggerLabel+1}Time', f'Logger{LoggerLabel+1}{feature}', data=df, label = f'Logger{LoggerLabel+1}')
        axs[1, 0].plot(f'Logger{LoggerLabel+2}Time', f'Logger{LoggerLabel+2}{feature}', data=df, label = f'Logger{LoggerLabel+2}')
        axs[1, 1].plot(f'Logger{LoggerLabel+3}Time', f'Logger{LoggerLabel+3}{feature}', data=df, label = f'Logger{LoggerLabel+3}')

    for i, ax in enumerate(axs.reshape(-1)):
        ax.axvline(x=jobFinishTime)
        ax.set_title(f'Position {i+1}')
        ax.legend()
    return jobFinishTime

if __name__ == "__main__":
    dataFolder = '30Jun'
    filePath = filePath = Path(r'C:\Users\TonyWitt\OneDrive - Evolve\Documents\Flir Logs')
    June30 = filePath/dataFolder
    July7 = filePath/'06Jul07Jul'


    job = July7
    dataLocation = pd.read_csv(job/'syncedData.csv')
    
    #featurePlotter(dataLocation,'Temp')
    #jobFinishTime = PositionSplitFeaturePlotter(dataLocation, 'Temp')
    jobFinishTime = splitFeaturePlotter(dataLocation, 'Humidity')
    plt.xlim([0,jobFinishTime+900])
    #plt.ylim([20,27])
    plt.suptitle('07Jul Control Data')
    plt.show(block=True)
    #plt.savefig(Path(r"C:\Users\TonyWitt\OneDrive - Evolve\Pictures")/str(job)[-5:])