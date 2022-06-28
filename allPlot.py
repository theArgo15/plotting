from ast import Not
from lib2to3.pgen2.pgen import DFAState
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def tempPlotter(df):
    fig, ax = plt.subplots()
    for column in df.columns:
        if 'Temp' in column:
            ax.plot('Time', column, data=df, label=column)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature ($^\circ$C)')
    ax.set_title('Title')
    ax.legend()

def RHPlotter(df):
        fig, ax = plt.subplots()
        for column in df.columns:
            if "Humidity" in column:
                ax.plot('Time', column, data=df, label=column)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Temperature ($^\circ$C)')
        ax.set_title('Title')
        ax.legend()
    

if __name__ == "__main__":
    tempPlotter(pd.read_csv('newNewData.csv'))
    RHPlotter(pd.read_csv('newNewData.csv'))
    plt.show(block=True)