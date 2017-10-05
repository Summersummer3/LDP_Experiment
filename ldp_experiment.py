# -*- coding: utf-8 -*-
# __author__ = 'summer'

import pymongo
import random
import math
import csv_writer
import rappor_sim

def create_data(distri, num, db, col):
    '''
    :param distri: distribution of all possible types.
    :param n: number of insert rows
    :param db: database name.
    :param col: collection name.
    :return: 
    '''

    if round(sum(distri), 3) != 1:
        print "error"
        return 0

    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]

    b_p = 0
    b_t = 0
    n = random.random()

    for i in xrange(num):
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
    conn.close()

def db_interface(db, col):
    '''
    :param db: database name.
    :param col: collection name.
    :return: the set of all queries.
    '''

    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]
    query = col.find()
    set = []
    for q in query:
        set.append(dict(q))
    conn.close()
    return set

def true_answer(size, set):
    '''
    :param size: size of types.
    :param set: the all queries. 
    :return: true answer of frequencies.
    '''

    res = [0] * size
    num = len(set)

    for i in set:
        index = i["type"]
        res[index] += 1

    res = list(map(lambda x: x * 1.0 / num, res))
    return res

def ldp_answer(size, set, eps, additive=False):
    '''
    :param size: 
    :param set: 
    :param eps: 
    :param additive: 
    :return: 
    '''

    res = [0] * size
    num = len(set)

    for i in set:
        index = i["type"]
        j = random.randint(0, size - 1)
        if not additive:
            if index == j:
                p = (math.e ** eps) / (math.e ** eps + 1)
            else:
                p = 1 / (math.e ** eps + 1)
        else:
            if index <= j:
                p = (math.e ** eps) / (math.e ** eps + 1)
            else:
                p = 1 / (math.e ** eps + 1)

        n = random.random()
        if n <= p:
            res[j] += (math.e ** eps) * size / (math.e ** eps - 1)
        else:
            res[j] += (-size) / (math.e ** eps - 1)

    if additive:
        res_tmp = [res[0]]
        for i in xrange(1, len(res)):
            res_tmp.append(res[i] - res[i - 1])
        res = res_tmp

    res = list(map(lambda x: x / num, res))
    return res

def consistency(res):
    '''
    :param res: 
    :return: 
    '''

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


if __name__ == '__main__':
    db = "dpdb"
    col = "exp1"
    num = 40000
    eps = 0.1
    #d = 20

    distri = [.08, .02, .05, .05, .01, .09, .03, .07, .11, .02, .04, .03, .05, .05, .13, .03, .02, .02, .04, .06]
    dic_len = len(distri)

    create_data(distri, num, db, col)

    set = db_interface(db, col)
    r_1 = true_answer(dic_len, set)

    while eps < 0.4:
        for i in xrange(10000):

            # r_2 = ldp_answer(dic_len, set, 0.5, additive=True)
            r_3 = ldp_answer(dic_len, set, eps)
            r_7 = consistency(r_3)
            # r_4 = rappor_answer(dic_len, set, 2.0)
            # r_5 = rappor_sim.rappor(dic_len, set, eps, type="sampling")
            # r_6 = rappor_sim.basic_rappor(dic_len, set, 0.25, 0.25)


            if not i:
                csv_writer.write_res(r_1, r_3, filename="result_" + str(eps) + ".csv", header=True)
                csv_writer.write_res(r_1, r_7, filename="result_consistency_" + str(eps) + ".csv", header=True)
                # write_res(r_1, r_4, filename="result_naive_rappor_" + str(eps) + ".csv", header=True)
                # csv_writer.write_res(r_1, r_5, filename="result_sampling_rappor_" + str(eps) + ".csv", header=True)
                # csv_writer.write_res(r_1, r_6, filename="result_basic_rappor_" + str(eps) + ".csv", header=True)

            else:
                csv_writer.write_res(r_1, r_3, filename="result_" + str(eps) + ".csv")
                csv_writer.write_res(r_1, r_7, filename="result_consistency_" + str(eps) + ".csv")
                # write_res(r_1, r_4, filename="result_naive_rappor_" + str(eps) + ".csv")
                # csv_writer.write_res(r_1, r_5, filename="result_sampling_rappor_" + str(eps) + ".csv")
                # csv_writer.write_res(r_1, r_6, filename="result_basic_rappor_" + str(eps) + ".csv")

            #when epsilon is small, (d is large?) the performance will be bad
        print "write_finish!!"
        eps += 0.2

