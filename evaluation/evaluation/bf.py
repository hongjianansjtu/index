#!/usr/bin/python
# Author: Jianan Hong
# Created Time: 2023-06-21 16:05:52
# Name: bf.py
import math
import mmh3
import numpy as np
from bitarray import bitarray


def dic2byte(obj):
    output = b'b:'
    for elem in obj.values():
        x = elem.to_bytes(16, 'big')
        output = output + x
    return output


def dict_to_str(d: dict):
    return str(sorted(d.items()))

class BloomFilter():
    def __init__(self, delta, n, theta):

        self.size = round(2.08 * delta * math.log(n / theta, math.e))
        self.hashnum = round(1.44 * math.log(n / theta, math.e))
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item):
        digests = []
        for i in range(self.hashnum):
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)
            self.bit_array[digest] = True

    def check(self, item):
        for i in range(self.hashnum):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True


if __name__ == '__main__':
    bf = BloomFilter(20, 100, 20)
    word_present = [{'id': 15000, 'height': 3}, {'id': 300, 'height': 100}]
    word_check = [{'id': 15000, 'height': 3}, {'id': 2400, 'height': 4}]
    for word in word_present:
        bf.add(dict_to_str(word))
    for word in word_check:
        print(bf.check(dict_to_str(word)))
    print(bf.__dict__)
