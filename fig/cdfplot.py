import matplotlib.pyplot as plt
from matplotlib import rcParams

params = {'font.family': 'serif',
          'font.serif': 'Times New Roman',
          # 'font.style':'italic',
          'font.weight': 'normal',  # or 'blod'
          'font.size': 16,  # or large,small
          }
rcParams.update(params)
import numpy as np
import pandas as pd

df = pd.read_csv('verify_overhead.csv')
labels = ['CH-based[10, 21]', 'BF[?]', 'Yu[22]', 'CertLedger[20]', 'AcBF']

my_array = df.to_numpy()
my_array = np.delete(my_array, 0, 1)


def get_hist_sum_list(hist):
    cnt = 0
    hist_sum_l = []
    hist_sum = sum(hist)
    for i in hist:
        cnt += i
        hist_sum_l.append(cnt / hist_sum)
    return hist_sum_l


# labels = ['BF[?]', 'Yu[22]', 'CertLedger[20]', 'AcBF']
bins_hist = 10000
range_hist = (0, 500)

hist0_, bin_edges0 = np.histogram(my_array[:, 0], bins=bins_hist, range=range_hist)
hist0 = get_hist_sum_list(hist0_)
plt.plot(bin_edges0[0:-1], hist0, label=labels[0])

hist1_, bin_edges1 = np.histogram(my_array[:, 1], bins=bins_hist, range=range_hist)
hist1 = get_hist_sum_list(hist1_)
plt.plot(bin_edges1[0:-1], hist1, label=labels[1])

hist2_, bin_edges2 = np.histogram(my_array[:, 2], bins=bins_hist, range=range_hist)
hist2 = get_hist_sum_list(hist2_)
plt.plot(bin_edges2[0:-1], hist2, label=labels[2])

hist3_, bin_edges3 = np.histogram(my_array[:, 3], bins=bins_hist, range=range_hist)
hist3 = get_hist_sum_list(hist3_)
plt.plot(bin_edges3[0:-1], hist3, label=labels[3])

hist4_, bin_edges4 = np.histogram(my_array[:, 4], bins=bins_hist, range=range_hist)
hist4 = get_hist_sum_list(hist4_)
plt.plot(bin_edges4[0:-1], hist4, label=labels[4])

plt.xlabel('Time Cost (ms)')
plt.legend()

plt.show()
