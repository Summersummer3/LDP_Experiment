# -*- coding: utf-8 -*-
# __author__ = 'summer'
# 1. create test itemset data
# 2. create dictionary for itemset

import pymongo
import random
import itertools

def create_itemset(size, n, p, db, col):
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
        item_set = []
        for j in xrange(size):
            r = random.random()
            if r <= p:
                item_set.append(j)
        data = {"items" : item_set}
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
        dic[i] = v
    return dic

if __name__ == '__main__':

    size = 10
    n = 200000
    k = 3
    db = "dpdb"
    col = "exp_itemset"
    # create_itemset(size, n, 0.3, db, col)

    d = create_reflect_dict(size, k)
    print d[5]