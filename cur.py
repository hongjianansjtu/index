#!/usr/bin/python
#Author: Jianan Hong
#Created Time: 2023-07-03 09:12:13
#Name: cur.py

from charm.toolbox.eccurve import secp224r1
from charm.toolbox.ecgroup import ECGroup, G, ZR

import random

groupObj = ECGroup(secp224r1)

g = group.random(G)
x = group.random(ZR)

y = g ** x

def chameleonHash(group, y, msg):
    r, s= group.random(ZR), group.random(ZR)
    ch = r - group.hash(y**group.hash((msg,r))*(g**s))
    return (r, s, ch)

def verifych(group, y, msg, r, s, ch):
    ch1 = r - group.hash(y**group.hash((msg,r))*(g**s))
    return ch==ch1

def ajust(group, x, msg, ch):
    k = group.random(ZR)
    r = ch + group.hash(g**k)
    s = k - x * group.hash((msg, r))
    return (r,s)

if __name__ == '__main__':

