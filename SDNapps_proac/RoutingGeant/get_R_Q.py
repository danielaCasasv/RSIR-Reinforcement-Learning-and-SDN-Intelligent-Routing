import copy
import numpy as np
def rand_number(seed):
    m = 2^34
    c = 251
    a = 4*c +1
    b = 351
    return ((a*seed+b)%m)/m

def gaussian(x, mu, sig):
    return round(np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))), 3)

def initial_R(A,Z,weight,A_Z_dict):
    #input net is
    R = {}
    net = copy.deepcopy(A_Z_dict)
    for i in net.keys():
        sub_key = net[i]
        sub_dic = {}
        for j in sub_key:
            sub_dic[j] = 0
        R[i] = sub_dic       
    for i in range(len(A)):
        R[A[i]][Z[i]] = weight[i]
    return R

def initial_Q(R):
    seed = np.random.randint(0, 100)
    Q = copy.deepcopy(R)
    for i in Q.keys():
        for j in Q[i].keys():
            # Q[i][j] = rand_number(seed)
            Q[i][j] = 0
    return Q