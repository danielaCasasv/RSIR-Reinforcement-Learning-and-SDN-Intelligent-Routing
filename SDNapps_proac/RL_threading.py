import sys
sys.path.insert(0,'/home/controlador/ryu/ryu/app/SDNapps_proac/RoutingGeant')
from main import get_all_paths
import pandas as pd
import time
import threading 
import bot
import json,ast
import csv
# THREADING

def paths_():
		data = pd.read_csv("/home/controlador/ryu/ryu/app/SDNapps_proac/net_info.csv")
		# print(data)
		paths, total_time = get_all_paths(data)
		threading.Timer(10, paths_).start()

def call_bot(msg):
        bot.sendMessage(msg)

def get_paths_base():
    file_base = '/home/controlador/ryu/ryu/app/SDNapps_proac/RoutingGeant/paths_weight.json'
    with open(file_base,'r') as json_file:
        paths_dict = json.load(json_file)
        paths_base = ast.literal_eval(json.dumps(paths_dict))
        return paths_base

def get_paths_RL():
    file_RL = '/home/controlador/ryu/ryu/app/SDNapps_proac/paths.json'
    with open(file_RL,'r') as json_file:
        paths_dict = json.load(json_file)
        paths_RL = ast.literal_eval(json.dumps(paths_dict))
        return paths_RL

def stretch(paths, paths_base, src, dst):
   
    if isinstance(paths.get(str(src)).get(str(dst))[0],list):
        # print (paths.get(str(src)).get(str(dst))[0],'----', paths_base.get(str(src)).get(str(dst)))
        add_stretch = float(len(paths.get(str(src)).get(str(dst))[0])) - float(len(paths_base.get(str(src)).get(str(dst))))
        mul_stretch = float(len(paths.get(str(src)).get(str(dst))[0])) / float(len(paths_base.get(str(src)).get(str(dst))))
        return add_stretch, mul_stretch
    else:
        # print (paths.get(str(src)).get(str(dst)),'----', paths_base.get(str(src)).get(str(dst)))
        add_stretch = float(len(paths.get(str(src)).get(str(dst)))) - float(len(paths_base.get(str(src)).get(str(dst))))
        mul_stretch = float(len(paths.get(str(src)).get(str(dst)))) / float(len(paths_base.get(str(src)).get(str(dst))))
        return add_stretch, mul_stretch

def calc_all_stretch(cont):
    paths_base = get_paths_base()
    paths_RL = get_paths_RL()
    cont_RL = 0
    total_paths = 0
    switches = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    a = time.time()
    with open('/home/controlador/ryu/ryu/app/SDNapps_proac/RoutingGeant/stretch/'+str(cont)+'_stretch.csv','wb') as csvfile:
        header = ['src','dst','add_st','mul_st']
        file = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file.writerow(header)
        for src in switches:
            for dst in switches:
                if src != dst:
                    total_paths += 1
                    add_stretch_RL, mul_stretch_RL = stretch(paths_RL, paths_base, src, dst)
                    if add_stretch_RL != 0:
                        cont_RL += 1
                    # print('Additive stretch RL: ', add_stretch_RL)
                    # print('Multi stretch RL: ', mul_stretch_RL)
                    file.writerow([src,dst,add_stretch_RL,mul_stretch_RL])
    total_time = time.time() - a
    return total_time

def RL_thread():
    cont = 0
    while cont < 836:
    # while cont < 30:
        a = time.time()
        data = pd.read_csv("/home/controlador/ryu/ryu/app/SDNapps_proac/net_info.csv")
        paths, time_RL = get_all_paths(data)
        # print('time_RL',time_RL)
        time_stretch = calc_all_stretch(cont)
        # print('time_stretch' , time_stretch)
        if time_RL > 10:
            time.sleep(time_RL + time_stretch)
        else:
            time.sleep(10 - time_RL - time_stretch)
        cont = cont + 1
        # print(time.time()-a)
RL_thread()
call_bot("RL-thread ended")
