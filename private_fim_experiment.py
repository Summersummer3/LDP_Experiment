# -*- coding: utf-8 -*-
# __author__ = 'summer'
# 1. create test itemset data
# 2. create dictionary for itemset

import pymongo
import random
import itertools
import math
import csv_writer

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


    for i in xrange(n):
        itemset = []
        for j in xrange(size):
            r = random.random()
            if r <= dist[j]:
                itemset.append(j)
        data = {"items": itemset}
        col.insert(data)

    print "insert success!"
    conn.close()


def create_reflect_dict(size, k):
    '''
    :param size: same as previous
    :param k: length of frequent subset itemsets
    :return: dict
    '''
    dic = {}
    c = list(itertools.combinations(xrange(size), k))
    for i, v in enumerate(c):
        dic[v] = i
    return dic

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
    set = []
    for q in query:
        set.append(dict(q))
    conn.close()
    return set

def true_answer(set, dic, k):
    '''
    :param set: true queries from database
    :param dic: the reflection dictionary
    :param k: length-k subset itemsets
    :return: ture answer 
    '''
    res = [0] * len(dic)
    num = len(set)
    for items in set:
        itemset = items['items']
        for subset in list(itertools.combinations(itemset, k)):
            res[dic[subset]] += 1
    res = list(map(lambda x: x * 1.0 / num, res))
    return res

def ldp_answer(set, lst, eps):
    length = len(lst)
    res = [0] * length
    for items in set:
        itemset = items['items']
        j = random.randint(0, length - 1)
        flag = True
        for i in list(lst[j][0]):
            if i not in itemset:
                flag = False
                break
        p = (math.e ** eps) / (math.e ** eps + 1) if flag else 1 / (math.e ** eps + 1)
        n = random.random()
        if n <= p:
            res[j] += (math.e ** eps) * length / (math.e ** eps - 1)
        else:
            res[j] += (-length) / (math.e ** eps - 1)

    res = list(map(lambda x: x / len(set), res))
    return res

if __name__ == '__main__':

    size = 10
    n = 200000
    k = 3
    db = "dpdb"
    col = "exp_itemset_1"
    dist = [0.8, 0.1, 0.3, 0.7, 0.7, 0.1, 0.2, 0.4, 0.2, 0.5]
    eps = 2.0

    # create_itemset(size, n, dist, db, col)
    dic = create_reflect_dict(size, k)
    set = db_interface(db, col)
    lst = sorted(list(dic.items()), key=lambda x: x[1])
    titles = []
    r_1 = true_answer(set, dic, k)

    for i in lst:
        titles.append(str(i[0]))

    for j in xrange(10):

        r_2 = ldp_answer(set, lst, eps)

        if not j:
            csv_writer.write_fim_res(r_1, r_2, filename="result_fim_" + str(eps) + ".csv", header=True, titles=titles)

        else:
            csv_writer.write_fim_res(r_1, r_2, filename="result_fim_" + str(eps) + ".csv", titles=titles)