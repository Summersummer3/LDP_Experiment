# -*- coding: utf-8 -*-
# __author__ = 'summer'
import csv

def count_error(r_1, r_2):
    res = 0
    for i in xrange(len(r_1)):
        res += (r_1[i] - r_2[i]) ** 2
    return res

def count_maxerror(r_1, r_2):
    m_error = 0
    for i in xrange(len(r_1)):
        error = abs(r_1[i] - r_2[i])
        if error > m_error:
            m_error = error
    return m_error

def write_res(r_1, r_2, r_c = None, filename="result.csv", header=False):

    headers = [i for i in xrange(len(r_1))]
    headers.append("error")
    headers.append("max_error")
    res_1 = count_error(r_1, r_2)
    res_2 = count_maxerror(r_1, r_2)
    row_1 = dict((k, v) for k, v in enumerate(r_1))
    row_2 = dict((k, v) for k, v in enumerate(r_2))
    row_2["error"] = res_1
    row_2["max_error"] = res_2
    rows = [row_1, row_2]

    if r_c:
        res_3 = count_error(r_1, r_2)
        res_4 = count_maxerror(r_1, r_2)
        row_3 = dict((k, v) for k, v in enumerate(r_c))
        row_3["error"] = res_3
        row_3["max_error"] = res_4
        rows.append(row_3)

    with open(filename, "ab") as f:
        f_csv = csv.DictWriter(f, headers)
        if header:
            f_csv.writeheader()
        f_csv.writerows(rows)
        f.close()

def write_fim_res(r_1, r_2, filename="result.csv", header=False, titles=None):
    headers = titles[:]
    res_1 = count_error(r_1, r_2)
    res_2 = count_maxerror(r_1, r_2)
    row_1 = dict(zip(headers, r_1))
    row_2 = dict(zip(headers, r_2))

    row_2['error'] = res_1
    row_2['max_error'] = res_2
    rows = [row_1, row_2]

    headers.append('error')
    headers.append('max_error')

    with open(filename, "ab") as f:
        f_csv = csv.DictWriter(f, headers)
        if header:
            f_csv.writeheader()
        f_csv.writerows(rows)
        f.close()
