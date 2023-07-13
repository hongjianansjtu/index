import math
#import pandas as pd
import matplotlib.pyplot as plt
#from bf import *


def BF_size(delta, n, theta):
    size = 2.08 * delta * math.log((n - delta) / theta, math.e) / 8000
    #print(size)
    return size

def total_BF(delta, error_rate):
    size = - delta * math.log(error_rate, math.e) / ((math.log(2, math.e)) ** 2) / 8000
    return size
# 空间 单位 B
Acc = (28 + 84 + 84) /1000.0  # delta, g2, g2 ** k

# 总注册数：500000，撤销数：2000
user_size  = 100000
max_revoke = [5000 * (i + 1) for i in range(10)]
theta = 10000
err1 = 0.0001
err2 = 0.0005
#x = [1000 * (i + 1) for i in range(10)]  # 受影响用户
# AcBF
plt.plot(max_revoke, [BF_size(i, user_size, theta) + Acc for i in max_revoke],  'o-', label='AcBF (ratio = 0.1)')
plt.plot(max_revoke, [BF_size(i, user_size, theta*2) + Acc for i in max_revoke],  'o--', label='AcBF (ratio = 0.2)')
# BF
plt.plot(max_revoke, [total_BF(i, err1) for i in max_revoke], '^-', label='BF (allowed error = 0.01%)')
plt.plot(max_revoke, [total_BF(i, err2) for i in max_revoke], '^--', label='BF (allowed error = 0.05%)')

plt.legend()
plt.xlabel('Expectation of Revoked Certificates')
plt.ylabel('Storage Overhead (kB)')
plt.title('Storage Overhead Comparison')
#plt.savefig('fig/storage_overhead.pdf')
plt.show()
