#!/usr/bin/python
#Author: Jianan Hong
#Created Time: 2023-07-18 11:49:51
#Name: drawbox.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv('rtt')

my_array = df.to_numpy()
my_array= np.hstack((my_array, my_array))
plt.boxplot(my_array, vert=True, patch_artist=True)
plt.show()
