import pandas as pd
import matplotlib.pyplot as plt

# stat1 = pd.read_csv('stat1.csv', index_col=0)
stat5 = pd.read_csv('stat5.csv', index_col=0)
# stat10 = pd.read_csv('stat10.csv', index_col=0)
# stat50 = pd.read_csv('stat50.csv', index_col=0)

height = 100

x = [i + 1 for i in range(height)]

# AcBF
# 更新witness
plt.plot(x, stat5['Acc_update'], label='AcBF - witness update', linewidth=1)
# 申请加入Acc
plt.plot(x, [stat5['New_acc_wit'][i] if stat5['Revoke'][i] > 0 else 0 for i in range(height)], label='AcBF - add to acc', linewidth=1)

# Acc
# 全部有效用户更新
plt.plot(x, [stat5['Valid_user_num'][i] if stat5['Revoke'][i] > 0 else 0 for i in range(height)], label='Acc', linewidth=1)

# CH
# 有修改区块内的有效用户
plt.plot(x, stat5['CH_update'], label='CH', linewidth=1)
# CH影响的区块数，图中几乎看不出来
# plt.plot(x, stat5['CH_update_block'], label='CH_blocks', linewidth=1)

plt.legend()
plt.xlabel('Rounds')
plt.ylabel('Users')
plt.title('Number of users to update')
plt.savefig('fig/update.pdf')
plt.show()
