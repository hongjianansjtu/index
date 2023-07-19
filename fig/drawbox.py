#!/usr/bin/python
#Author: Jianan Hong
#Created Time: 2023-07-18 11:49:51
#Name: drawbox.py
import matplotlib.pyplot as plt
from matplotlib import rcParams 
params={'font.family':'serif',
        'font.serif':'Times New Roman',
        #'font.style':'italic',
        'font.weight':'normal', #or 'blod'
        'font.size':16,#or large,small
        }
rcParams.update(params)
import numpy as np
import pandas as pd
df = pd.read_csv('update_overhead.csv')
labels = ['CH-based[10, 21]', 'Yu[22]', 'CertLedger[20]', 'AcBF']
my_array = df.to_numpy()
my_array = np.delete(my_array, 0, 1)
#print(my_array)
#my_array= np.hstack((my_array, my_array))
bp = plt.boxplot(my_array, vert=True, showmeans = True, meanline = True,
            patch_artist=True, 
            labels=labels,
            medianprops = dict(linewidth = 1.5))
plt.ylabel('Time Cost (ms)')
bp['boxes'][0].set_facecolor('pink')
bp['boxes'][2].set_facecolor('lightgreen')
#plt.yscale('symlog', linthresh=0.01)
plt.show()
