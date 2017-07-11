# -*- coding: utf-8 -*-
# __author__ = 'summer'

import pymongo
import random
import math
import csv

def create_data(distri, db, col):
    print sum(distri) != 1
    if round(sum(distri), 3) != 1:
        print "error"
        return 0

    Client = pymongo.MongoClient("localhost", 27017)
    db = Client[db]
    col = db[col]

    b_p = 0
    b_t = 0
    n = random.random()

    for p in distri:
        if n <= b_p + p:
            type = b_t
            break
        else:
            b_p += p
            b_t += 1

    data = {"type": type}
    col.insert(data)
    print "insert success"

def true_answer(size, db, col):
    res = [0] * size
    Client = pymongo.MongoClient("localhost", 27017)
    db = Client[db]
    col = db[col]

    set = col.find()
    num = set.count()

    for i in set:
        index = i["type"]
        res[index] += 1

    res = list(map(lambda x: x * 1.0 / num, res))
    return res

def ldp_answer(size, db, col, eps):
    res = [0] * size
    Client = pymongo.MongoClient("localhost", 27017)
    db = Client[db]
    col = db[col]
    set = col.find()
    num = set.count()

    for i in set:
        index = i["type"]
        j = random.randint(0, size - 1)
        if index == j:
            p = (math.e ** eps) / (math.e ** eps + 1)
        else:
            p = 1 / (math.e ** eps + 1)

        n = random.random()
        if n <= p:
            res[j] += (math.e ** eps) * size / (math.e ** eps - 1)
        else:
            res[j] += (-size) / (math.e ** eps - 1)

    res = list(map(lambda x: x / num, res))
    return res

def consistency(res):
    r_c = []
    r = []
    r_c.append(res[0] * 1.0)
    for w in xrange(1, len(res)):
        r_c.append(res[w] + r_c[w - 1] * 1.0)

    for k in xrange(0, len(r_c)):
        max = 0
        for i in xrange(0, k + 1):
            for j in xrange(i, len(r_c)):
                s = sum(r_c[i : j + 1])
                if j == i:
                    min = s
                elif min > s / (j - i + 1):
                    min = s / (j - i + 1)
            if min > max:
                max = min
        r.append(max)

    out = []
    for v in xrange(len(r)):
        if not v:
            out.append(r[v])
        else:
            out.append(r[v] - r[v - 1])
    return out

def count_error(r_1, r_2):
    res = 0
    for i in xrange(len(r_1)):
        res += (r_1[i] - r_2[i]) ** 2
    return res

def write_res(r_1, r_2, r_c = None, filename="result.csv"):
    headers = [i for i in xrange(len(r_1))]
    headers.append("error")
    res_1 = count_error(r_1, r_2)
    row_1 = dict((k, v) for k, v in enumerate(r_1))
    row_2 = dict((k, v) for k, v in enumerate(r_2))
    row_2["error"] = res_1
    rows = [row_1, row_2]

    if r_c:
        res_2 = count_error(r_1, r_c)
        row_3 = dict((k, v) for k, v in enumerate(r_c))
        row_3["error"] = res_2
        rows.append(row_3)

    with open(filename, "ab") as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
        f.close()

if __name__ == '__main__':
    db = "dpdb"
    col = "exp1"
    #d = 20

    distri = [.08, .02, .05, .05, .01, .09, .03, .07, .11, .02, .04, .03, .05, .05, .13, .03, .02, .02, .04, .06]
    dic_len = len(distri)

    # n = 0
    # while n < 40000:
    #     create_data(distri, db, col)
    #     n += 1
    for i in xrange(20):
        r_1 = true_answer(dic_len, db, col)
        r_2 = ldp_answer(dic_len, db, col, 0.5)
        for j in xrange(len(r_2)):
            if r_2[j] < 0:
                r_c = consistency(r_2)
                write_res(r_1, r_2, r_c=r_c, filename="result0.5,20.csv")
                break
            elif j == len(r_2) - 1:
                write_res(r_1, r_2, filename="result0.5,20.csv")

    #when epsilon is small, d is large the performance will be bad



