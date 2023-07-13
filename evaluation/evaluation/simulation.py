#!/usr/bin/python
# Author: Jianan Hong
# Created Time: 2023-05-30 10:48:30
# Name: id.py

import pandas as pd
import numpy as np
from bf import *


def dict_to_str(d: dict):
    return str(sorted(d.items()))


height = 100

regis_event = np.random.poisson(1000, height)
revoke_event = [int(i) for i in np.floor(np.random.exponential(50, height - 20))]
print(revoke_event)
acbf = BloomFilter(4000, 96000, 9600)
# 'Time': 轮次, 'Register': 本轮注册数, 'Valid_user_num': 总有效用户, 'Revoke': 本轮撤销数, 'Revoked_user_num': 总撤销用户,
# 'BF_false_positive': BF总误判数, 'New_acc_wit': 本轮新加入Acc数, 'Revoke_in_acc': 本轮从Acc中删除数,
# 'Acc_update': 本轮需要更新Acc witness的用户数, 'BF_false_positive_rate': 当前总的BF误判率,
# 'CH_update': 使用变色龙哈希时需要更新默克尔证明的数目, 'CH_update_block': 有多少个区块需要更新
# 统计acc更新的运算次数
stat_data = {'Time': [], 'Register': [], 'Valid_user_num': [], 'Revoke': [], 'Revoked_user_num': [],
             'BF_false_positive': [], 'New_acc_wit': [], 'Revoke_in_acc': [], 'Acc_update': [],
             'BF_false_positive_rate': [], 'CH_update_block': [], 'CH_update': []}

user_cert = []
user_revoke = []
x_count = 1
acc = set()
fp = 0


def register():
    global user_cert
    pass


def revoke(i, current_revoke):
    global user_revoke, acbf
    acc_del = 0
    for index in current_revoke:
        user_revoke.append({'time': i, 'id': user_cert[index]['id'], 'height': user_cert[index]['height']})
        # acc check, wit update
        if dict_to_str(user_cert[index]) in acc:
            acc_del += 1
        acbf.add(dict_to_str(user_cert[index]))
    return acc_del


def update(i):
    global user_revoke, user_cert, acbf, regis_event
    fp_t = 0
    ch_t = 0
    revoke_height = set()
    for index in user_revoke:
        if index['time'] == i:
            try:
                user_cert.remove({'id': index['id'], 'height': index['height']})
                regis_event[index['height']] -= 1
                revoke_height.add(index['height'])
            except ValueError:
                pass
    for index in user_cert:
        if acbf.check(dict_to_str(index)) == True:
            fp_t += 1
            acc.add(dict_to_str(index))
    for h in revoke_height:
        ch_t += regis_event[h]
    return fp_t, ch_t, len(revoke_height)


for i in range(np.prod(regis_event.shape)):
    print(i)
    for num in range(regis_event[i]):
        user_cert.append({'id': x_count, 'height': i})
        x_count += 1
    stat_data['Time'].append(i)
    stat_data['Register'].append(regis_event[i])
    if i >= 20:
        current_revoke = np.random.randint(0, len(user_cert), revoke_event[i - 20])
        # 撤销
        acc_del_i = revoke(i, current_revoke)
        # 撤销后其余信息更新
        fp_i, ch_i, chb_i = update(i)

        # 数据统计
        stat_data['Acc_update'].append((stat_data['BF_false_positive'][-1] - acc_del_i) if acc_del_i != 0 else 0)
        stat_data['New_acc_wit'].append(fp_i + acc_del_i - stat_data['BF_false_positive'][-1])
        stat_data['BF_false_positive'].append(fp_i)
        stat_data['Revoke'].append(revoke_event[i - 20])
        stat_data['Revoked_user_num'].append(len(user_revoke))
        stat_data['Revoke_in_acc'].append(acc_del_i)
        stat_data['Valid_user_num'].append(len(user_cert))
        stat_data['BF_false_positive_rate'].append(format(fp_i / len(user_cert), '.4f'))
        stat_data['CH_update_block'].append(chb_i)
        stat_data['CH_update'].append(ch_i)

    else:
        stat_data['Acc_update'].append(0)
        stat_data['New_acc_wit'].append(0)
        stat_data['BF_false_positive'].append(0)
        stat_data['Revoke'].append(0)
        stat_data['Revoked_user_num'].append(0)
        stat_data['Revoke_in_acc'].append(0)
        stat_data['Valid_user_num'].append(len(user_cert))
        stat_data['BF_false_positive_rate'].append(format(0.0, '.4f'))
        stat_data['CH_update_block'].append(0)
        stat_data['CH_update'].append(0)

print(len(user_revoke))
print(len(user_cert))

print(x_count)
print(user_revoke)

print(acbf.__dict__)

df = pd.DataFrame(stat_data)
df.to_csv('stat.csv', index=False)
