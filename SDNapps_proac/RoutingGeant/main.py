from get_dict import get_dict
from get_R_Q import initial_R, initial_Q
from get_result import get_result
import pandas as pd
import time
import json

def RL_forwarding(data, src, dst):
    
    graph = get_dict(data)

    A = graph["A"]
    Z = graph["Z"]
    weight = graph["weight"]
    links = graph["links"]

    R = initial_R(A,Z,weight,links)
    Q = initial_Q(R)

    alpha = 0.9 # learning rate
    epsilon = 0.8 #greedy policy
    n_episodes = 300

    return get_result(R,Q,alpha,epsilon,n_episodes,src,dst)

def get_all_paths(data):
    time_init = time.time()
    graph = get_dict(data)
    links = graph["links"]
    sws = list(links.keys())
    
    paths = {}
    for i in sws:
        paths.setdefault(i, {})
        for j in sws:
            if i != j:
                j = [j]
                time0 = time.time()
                result = RL_forwarding(data,i,j)
                
                if j[0] not in paths[i]:
                    paths[i][j[0]] = result["all_routes"][j[-1]]
    with open('/home/controlador/ryu/ryu/app/SDNapps_proac/paths.json','w') as json_file:
        json.dump(paths, json_file, indent=2)
    time_end = time.time()
    total_time = time_end - time_init
    
    with open('/home/controlador/ryu/ryu/app/SDNapps_proac/times.txt','a') as txt_file:
        txt_file.write(str(total_time)+'\n')

    # For testing ---------------------------------
    print("ok") #aaa
    # print("Final dict paths: {0}".format(paths))
    # print("execute",time.ctime())
    # print("total time:" , total_time)
    #---------------------------------------------
    return paths, total_time

#For testing-------------------------------
# file ='/home/controlador/ryu/ryu/app/SDNapps_proac/net_info.csv'
# data = pd.read_csv(file)
# get_all_paths(data)