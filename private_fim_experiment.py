# -*- coding: utf-8 -*-
# __author__ = 'summer'
# 1. create test itemset data
# 2. create dictionary for itemset

import pymongo
import random
import math
import csv_writer

class Itemset:
    def __init__(self, pattern, count=1, n=1):
        self.pattern = pattern
        self.count = count
        self.n = n
        self.freq = 0

    def set_freq(self, freq=0):
        self.freq = freq if freq else self.count * 1.0 / self.n

    def out(self):
        print (self.pattern, self.freq)


def create_itemset(size, n, dist, db, col):
    '''
    :param size: size of possible items.
    :param n: number of insert item sets.
    :param p: the probability to include the item for one row.
    :param db: database name.
    :param col: collection name.
    :return: 
    '''
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]
    if size != len(dist):
        return -1

    for i in xrange(n):
        itemset = []
        for j in xrange(1, size + 1):
            r = random.random()
            if r <= dist[j - 1]:
                itemset.append(j)
        data = {"items": itemset}
        col.insert(data)

    print "insert success!"
    conn.close()
    return 0


def db_query_interface(db, col, type="i"):
    '''
    :param db: 
    :param col: 
    :return: big set 
    '''
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]
    query = col.find()
    if type == "i":
        T = []
        for q in query:
            T.append(list(q["items"]))
        conn.close()
        return T

    if type == "r":
        L = []
        for q in query:
            itemset = Itemset(set(list(q["itemset"])))
            itemset.set_freq(q["freq"])
            L.append(itemset)
        conn.close()
        return L


def db_insert_interface(db, col, lst):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]
    for itemset in lst:
        data = {"itemset": list(itemset.pattern),
                "freq": itemset.freq}
        col.insert(data)
    conn.close()
    return 0


def init_domain(size):
    return list(map(lambda x: set([x]), range(1, size + 1)))


# def create_reflect_dict(size, k):
#     '''
#     :param size: same as previous
#     :param k: length of frequent subset itemsets
#     :return: dict
#     '''
#     dic = {}
#     c = list(itertools.combinations(xrange(size), k))
#     for i, v in enumerate(c):
#         dic[set(v)] = i
#     return dic



def apriori(T, domain, l, phi):
    '''
    :param set: true queries from database
    :param dic: the reflection dictionary
    :param l: length less than l itemsets
    :return: frequent itemset
    '''
    l_now = 1
    L = []
    C_f = []
    C = []
    n = len(T)
    while l_now <= l and len(domain) > 0:
        for t in T:
            for itemset in domain:
                if satisfy(t, itemset):
                    C_f.append(Itemset(itemset, n=n))

            for c_f in C_f:
                if not len(C):
                    C.append(c_f)
                else:
                    for c in C:
                        if c_f.pattern == c.pattern:
                            c.count += 1
                            break
                    else:
                        C.append(c_f)
                C_f = []

        domain = []
        for c in C:
            c.set_freq()
            if c.freq >= phi:
                L.append(c)
                domain.append(c.pattern)

        domain = extension(domain)

        C = []
        l_now += 1
        print "length:" + str(l_now)
        print domain

    return L

def ldp_apriori(T, domain, eps, l, phi):

    n = len(T)
    L = []
    l_now = 1

    while len(domain) > 0 and l_now <= l:

        size = len(domain)
        res = [0] * size

        for t in T:
            j = random.randint(0, size - 1)
            p = (math.e ** eps) / (math.e ** eps + 1) if satisfy(t, domain[j]) else 1 / (math.e ** eps + 1)
            r_seed = random.random()
            if r_seed <= p:
                res[j] += (math.e ** eps) * size / (math.e ** eps - 1)
            else:
                res[j] += (-size) / (math.e ** eps - 1)

        res = list(map(lambda x: x / n, res))

        domain_tmp = []
        for i in xrange(size):
            if res[i] >= phi:
                itemset = Itemset(pattern=domain[i])
                itemset.set_freq(res[i])
                L.append(itemset)
                domain_tmp.append(itemset.pattern)
        domain = extension(domain_tmp)
        l_now += 1

    return L

def satisfy(t, itemset):
    lst = list(itemset)
    for i in lst:
        if i not in t:
            return False
    else:
        return True

def extension(lst):
    f_set = []

    if not len(lst):
        return []

    l = len(lst[0])
    for i in xrange(len(lst)):
        for j in xrange(i + 1, len(lst)):
            set_A = lst[i].copy()
            set_B = lst[j].copy()
            inter_set = list(set_A & set_B)
            if len(inter_set) != l - 1:
                continue
            diff = set_B.difference(set_A).pop()
            for inter in inter_set:
                tmp = set_A.copy()
                tmp.remove(inter)
                tmp.add(diff)
                if tmp not in lst:
                    break
            else:
                set_A.add(diff)
                if set_A not in f_set:
                    f_set.append(set_A)
    return f_set


def scores(L, L_dp, T):

    n = len(T)
    size_L = len(L)
    size_L_dp = len(L_dp)
    error = []
    count = 0

    if not (size_L_dp and size_L):
        print "At least one input is empty set"
        return 0

    for i_1 in L:
        for i_2 in L_dp:
            if i_1.pattern == i_2.pattern:
                count += 1
                error.append(abs(i_1.freq - i_2.freq))
                L_dp.remove(i_2)

    score_c = count * 1.0 / size_L
    score_s = len(L_dp) * 1.0 / size_L_dp

    for itemset in L_dp:
        count_t = 0
        for t in T:
            if satisfy(t, itemset.pattern):
                count_t += 1
        freq = count_t * 1.0 / n
        error.append(abs(freq - itemset.freq))

    max_error = max(error)

    return score_c, score_s, max_error



if __name__ == '__main__':

    size = 20
    n = 500000
    k = 3
    db = "dpdb"
    col = "exp_itemset_2"
    col_mining_result = "mining_result"

    # dist = []
    # for i in xrange(size):
    #     dist.append(round(random.random(), 3))
    #
    eps = 2.0
    #
    # print dist
    #
    # ret = create_itemset(size, n, dist, db, col)
    # if ret < 0:
    #     print "Wrong distribution!"

    domain = init_domain(size)

    T = db_query_interface(db, col)

    # print "data read complete!"
    # L_1 = apriori(T, domain, 5, 0.2)
    # flag = db_insert_interface(db, col_mining_result, L_1)
    # if not flag:
    #     print "insert complete!"

    L = db_query_interface(db, col_mining_result, type="r")
    for i in L:
        i.out()


    # domain_test = init_domain(5)
    # T_test = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    # L_1 = apriori(T_test, domain_test, 3, 0.5)
    # flag = db_insert_interface(db, col_mining_result, L_1)
    # if not flag:
    #     print "insert complete!"
    # L = db_query_interface(db, col_mining_result, type="r")
    # for i in L:
    #     i.out()
    #
    # L_dp = ldp_apriori(T_test, domain_test, eps, 3, 0.5)
    # for j in L_dp:
    #     j.out()
    #
    # s_1, s_2, accuracy = scores(L, L_dp, T_test)
    # print s_1, s_2, accuracy




    L_2 = ldp_apriori(T, domain, eps, 5, 0.2)

    s_1, s_2, accuracy = scores(L, L_2, T)
    print s_1, s_2, accuracy

    # res_2 = ldp_apriori(T, domain, eps, 5, 0.2)
    # for r_2 in res_2:
    #     r_2.out()



    # titles = []
    # r_1 = true_answer(set, dic, k)
    #
    # for i in lst:
    #     titles.append(str(i[0]))
    #
    # for j in xrange(10):
    #
    #     r_2 = ldp_answer(set, lst, eps)
    #
    #     if not j:
    #         csv_writer.write_fim_res(r_1, r_2, filename="result_fim_" + str(eps) + ".csv", header=True, titles=titles)
    #
    #     else:
    #         csv_writer.write_fim_res(r_1, r_2, filename="result_fim_" + str(eps) + ".csv", titles=titles)