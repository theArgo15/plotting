from cProfile import label
from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

overallTitle = 'Ep Temperatures Over Time'
svp2Job = pd.read_excel('1656084383_appLogs.xlsx')



fig, ax = plt.subplots()
ax.plot('Time', 'EPTemp', data=svp2Job, label='EPTemp')
ax.plot('Time', 'ECSReturnTemp', data=svp2Job, label='ECSReturnTemp')
ax.plot('Layer', 'EPTemp', data=svp2Job, label='layer')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature ($^\circ$C)')
ax.set_title(overallTitle)
ax.legend()

if __name__ == "__main__":
    plt.show(block=True)
