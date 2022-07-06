from ast import Not
from lib2to3.pgen2.pgen import DFAState
from tkinter.tix import Tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def tempPlotter(df):
    fig, ax = plt.subplots()
    colormap = plt.cm.nipy_spectral
    colors = [colormap(i) for i in np.linspace(0, 1,21)]
    ax.set_prop_cycle('color', colors)
    for column in df.columns:
        if 'Temp' in column:
            if 'Logger' in column:
                ax.plot(f'Logger{column[6]}Time', column, data=df, label=column)
            else:
                ax.plot('Time', column, data=df, label=column)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature ($^\circ$C)')
    ax.set_title('Temperature 3 Hour Job 30JUN SVP0 Control')
    ax.legend()


def RHPlotter(df):
        fig, ax = plt.subplots()
        colormap = plt.cm.nipy_spectral
        colors = [colormap(i) for i in np.linspace(0, 1,21)]
        ax.set_prop_cycle('color', colors)
        for column in df.columns:
            if "Humidity" in column:
                if 'Logger' in column:
                    ax.plot(f'Logger{column[6]}Time', column, data=df, label=column)
                else:
                    ax.plot('Time', column, data=df, label=column)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Relative Humidity (%)')
        ax.set_title('Humidity Over Time')
        ax.legend()

def splitTempPlotter(df):
    fig, axs = plt.subplots(2,2, sharex=True, sharey=True)
    for i in range(4):
        axs[0, 0].plot(f'Logger{i+1}Time', f'Logger{i+1}Temp', data=df, label = f'Logger{i+1}')
    axs[0, 0].set_title('Engine 1')
    axs[0,0].legend()
    for i in range(4):
        axs[0, 1].plot(f'Logger{i+5}Time', f'Logger{i+5}Temp', data=df, label = f'Logger{i+5}')
    axs[0, 1].set_title('Engine 2')
    axs[0,1].legend()
    for i in range(4):
        axs[1, 0].plot(f'Logger{i+9}Time', f'Logger{i+9}Temp', data=df, label = f'Logger{i+9}')
    axs[1, 0].set_title('Engine 3')
    for i in range(4):
        axs[1, 1].plot(f'Logger{i+13}Time', f'Logger{i+13}Temp', data=df, label = f'Logger{i+13}')
    axs[1, 1].set_title('Engine 4')

if __name__ == "__main__":
    filePath = filePath = Path(r'C:\Users\TonyWitt\OneDrive - Evolve\Documents\Flir Logs\30Jun')
    dataLocation = pd.read_csv(filePath/'syncedData.csv')
    #tempPlotter(pd.read_csv(filePath/'syncedData.csv'))
    #RHPlotter(pd.read_csv(filePath/'syncedData.csv'))
    splitTempPlotter(dataLocation)
    plt.xlim([0,20000])
    plt.ylim([20,27])
    plt.show(block=True)