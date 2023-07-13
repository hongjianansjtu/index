import math
import pandas as pd
import matplotlib.pyplot as plt

stat = pd.read_csv('stat.csv', index_col=0)

height = 100

def cal_BF_space(n, fp):
    return int(math.ceil((-n * math.log(fp)) / (math.log(2) ** 2 * 8)))


# 空间 单位 B
BF_s = cal_BF_space(2000, 0.2)
Acc_s = 28 + 84 + 84
MP_s = 32 * 4

# 时间 单位 ms
BF_t = 0.001  # ?
Acc_verify_t = 0.66  # ?
Acc_witness_t = 0.66
Acc_update_t = 0.68

# CH_hash_t = 0.47
# CH_modify_t = 0.23

x = [i + 1 for i in range(height)]

plt.plot(x, stat['Register'], label='Register', linewidth=1)
plt.plot(x, stat['Revoke'], label='Revoke', linewidth=1)
plt.plot(x, stat['Valid_user_num'], label='Valid_user_num', linewidth=1)
plt.plot(x, stat['Revoked_user_num'], label='Revoked_user_num', linewidth=1)
plt.plot(x, stat['BF_false_positive'], label='BF_false_positive', linewidth=1)

plt.plot(x, stat['New_acc_wit'], label='New_acc_wit', linewidth=1)
plt.plot(x, stat['Revoke_in_acc'], label='Revoke_in_acc', linewidth=1)

plt.legend()
plt.xlabel('Round')
plt.ylabel('Count')
plt.title('Data Showing')
plt.savefig('Data_Showing.pdf')
plt.show()

# AcBF
plt.plot(x, [(BF_t * stat['Valid_user_num'][i] + Acc_verify_t * stat['BF_false_positive'][i]) / stat['Valid_user_num'][i] for i in range(height)],
         label='AcBF', linewidth=1)
# Acc
plt.plot(x, [Acc_verify_t for i in range(height)], label='Acc', linewidth=1)
# BF
plt.plot(x, [BF_t for i in range(height)], label='BF', linewidth=1)
# CH
plt.plot(x, [0 for _ in range(height)], label='CH', linewidth=1)

plt.legend()
plt.xlabel('Round')
plt.ylabel('Time Overhead(ms)')
plt.title('Time Overhead Comparison')
plt.savefig('Time_Overhead.pdf')
plt.show()


# AcBF
plt.plot(x, [(BF_t * stat['Valid_user_num'][i] + Acc_verify_t * stat['BF_false_positive'][i]) / stat['Valid_user_num'][i] for i in range(height)],
         label='AcBF', linewidth=1)
# Acc
plt.plot(x, [Acc_verify_t for i in range(height)], label='Acc', linewidth=1)
# BF
plt.plot(x, [BF_t for i in range(height)], label='BF', linewidth=1)
# CH
plt.plot(x, [0 for _ in range(height)], label='CH', linewidth=1)

plt.legend()
plt.xlabel('Round')
plt.ylabel('Storage Overhead(ms)')
plt.title('Storage Overhead Comparison')
plt.savefig('Storage_Overhead.pdf')
plt.show()

