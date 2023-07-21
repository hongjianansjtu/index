import pandas as pd
import random

mht_hash_time = 0
bf_time = 0

df1 = pd.read_csv('time_for_claimAccumulator', header=None)
claimAccumulator = df1.to_numpy().transpose().tolist()[0]

df2 = pd.read_csv('time_for_update_witness', header=None)
update_witness = df2.to_numpy().transpose().tolist()[0]

df3 = pd.read_csv('time_for_verify_ECDSA', header=None)
verify_ECDSA = df3.to_numpy().transpose().tolist()[0]

df4 = pd.read_csv('rtt', header=None)
rtt = df4.to_numpy().transpose().tolist()[0]

stat = pd.read_csv('stat.csv', header=None)
last_round = stat.iloc[-1:]

print(last_round)

valid_users = int(last_round.iloc[:, 2])
fp_users = int(last_round.iloc[:, 5])
print(valid_users)
print(fp_users)

verify_overhead = {'id': [], 'CH': [], 'BF': [], 'Acc': [], 'MHT': [], 'AcBF': []}

for i in range(valid_users):
    verify_overhead['id'].append(i)
    verify_overhead['MHT'].append(verify_ECDSA[random.randint(0, 999)] + mht_hash_time)
    verify_overhead['Acc'].append(verify_ECDSA[random.randint(0, 999)] + claimAccumulator[random.randint(0, 999)])
    verify_overhead['CH'].append(verify_ECDSA[random.randint(0, 999)] + rtt[random.randint(0, 1499)])
    verify_overhead['BF'].append(verify_ECDSA[random.randint(0, 999)] + bf_time)
    verify_overhead['AcBF'].append(verify_ECDSA[random.randint(0, 999)] + bf_time)

# AcBF错判用户加时
acbf_fp_users_list = random.sample([i for i in range(valid_users)], fp_users)
for i in acbf_fp_users_list:
    verify_overhead['AcBF'][i] += claimAccumulator[random.randint(0, 999)]

# BF错判用户加时
bf_fp_users_list = random.sample([i for i in range(valid_users)], round(valid_users * 0.0005))
for i in bf_fp_users_list:
    verify_overhead['BF'][i] += rtt[random.randint(0, 999)]

df = pd.DataFrame(verify_overhead)
df.to_csv('verify_overhead.csv', index=False)
