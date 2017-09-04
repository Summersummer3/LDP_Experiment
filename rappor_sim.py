# -*- coding: utf-8 -*-
# __author__ = 'summer'
import math
import random

def rappor(size, set, eps, type="naive"):
    res = [0] * size
    num = len(set)

    if type == "naive":
        p = math.e ** (eps / (2 * size)) / (1 + math.e ** (eps / (2 * size)))
    else:
        p = math.e ** (eps / 2) / (1 + math.e ** (eps / 2))

    for i in set:
        index = i["type"]

        if type == "naive":
            for j in xrange(size):
                r_seed = random.random()
                if r_seed <= p:
                    if index == j:
                        res[j] += 1
                else:
                    if index != j:
                        res[j] += 1

        elif type == "sampling":
            k = random.randint(0, size - 1)
            r_seed = random.random()
            if r_seed <= p:
                if index == k:
                    res[k] += size
            else:
                if index != k:
                    res[k] += size

    # c = c * c_\epsilon where c_\epsilon = 1 / (1 - 2p)
    res = list(map(lambda x: x * 1.0 / num, res))
    res = list(map(lambda x: (x + p - 1) / (2 * p - 1), res))
    return res

def basic_rappor(size, set, f, q):
    p = 1 - q
    res = [0] * size
    num = len(set)
    for i in set:
        index = i["type"]
        item = [0] * size
        item[index] = 1
        for n, v in enumerate(item):
            r_1 = random.random()
            #step 1:
            if r_1 <= 0.5 * f:
                item[n] = 0 if v == 1 else 1
            #step 2:
            r_2 = random.random()
            if r_2 <= q:
                item[n] = 0 if item[n] == 1 else 1
            res[n] += item[n]

    res = list(map(lambda x: (x - (q + 0.5 * f * p - 0.5 * f * q) * num) / ((1 - f) * (p - q) * num), res))
    return res






