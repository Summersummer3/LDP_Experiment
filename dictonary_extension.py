# -*- coding: utf-8 -*-
# __author__ = 'summer'

def extension(lst):
    f_set = []
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

lst = [set([1, 2, 3]), set([1, 4, 5]), set([1, 2, 4]), set([1, 3, 4]), set([2, 3, 4]), set([1 ,4, 6]), set([1, 5, 6]),
        set([4, 5, 6])]
print extension(lst)










