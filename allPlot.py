from ast import Not
from lib2to3.pgen2.pgen import DFAState
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
    ax.set_title('Temperature Over Time')
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
    

if __name__ == "__main__":
    filePath = filePath = Path(r'C:\Users\TonyWitt\OneDrive - Evolve\Documents\Flir Logs\30Jun')
    #tempPlotter(pd.read_csv(filePath/'syncedData.csv'))
    RHPlotter(pd.read_csv(filePath/'syncedData.csv'))
    plt.show(block=True)