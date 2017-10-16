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

    def out(self):
        print (self.pattern, self.count * 1.0 / self.n)


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
        print data
        col.insert(data)

    print "insert success!"
    conn.close()
    return 0


def db_interface(db, col):
    '''
    :param db: 
    :param col: 
    :return: big set 
    '''
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn[db]
    col = db[col]
    query = col.find()
    T = []
    for q in query:
        T.append(list(q["items"]))
    conn.close()
    return T


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
            if (c.count * 1.0 / n) >= phi:
                L.append(c)
                domain.append(c.pattern)

        domain = extension(domain)
        C = []
        l_now += 1
    return L

def ldp_apriori(T, domain, eps, l, phi):

    n = len(T)
    print n
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
        print res

        domain_tmp = []
        for i in xrange(size):
            if res[i] >= phi:
                itemset = Itemset(pattern=domain[i], count=res[i])
                L.append(itemset)
                domain_tmp.append(itemset.pattern)
        domain = extension(domain_tmp)
        domain_tmp = []
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




if __name__ == '__main__':

    size = 10
    n = 300000
    k = 3
    db = "dpdb"
    col = "exp_itemset_1"
    dist = [0.8, 0.1, 0.3, 0.7, 0.7, 0.4, 0.2, 0.4, 0.2, 0.9]
    eps = 2.0

    # ret = create_itemset(size, n, dist, db, col)
    # if ret < 0:
    #     print "Wrong distribution!"

    domain = init_domain(size)

    T = db_interface(db, col)
    # res = apriori(T, domain, 5, 0.15)
    # for r in res:
    #     r.out()
    res_1 = ldp_apriori(T, domain, eps, 5, 0.15)
    for r in res_1:
        r.out()

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