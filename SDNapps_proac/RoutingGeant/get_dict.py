import csv

def normalize(value, minD, maxD, min_val, max_val):
    if max_val == min_val:
        value_n = (maxD + minD) / 2 
    else:
        value_n = (maxD - minD) * (value - min_val) / (max_val - min_val) + minD
    return value_n

def normalize_path_cost(bwd, delay, pkloss):
    '''
    Normalize values for reward. 
    '''

    bwd_cost = [] #since the RL will minimize reward function, we do 1/bwd for such function
    for val in bwd:
        if val > 0.005: #ensure minimum bwd available
            temp = 1/val
            bwd_cost.append(round(temp, 6))
        else:
            bwd_cost.append(1/0.005)
    
    bwd_n = [normalize(bwd_val, 0, 100, min(bwd_cost), max(bwd_cost)) for bwd_val in bwd_cost]
    delay_n = [normalize(delay_val, 0, 100, min(delay), max(delay)) for delay_val in delay]
    pkloss_n = [normalize(pkloss_val, 0, 100, min(pkloss), max(pkloss)) for pkloss_val in pkloss]
    return bwd_n, delay_n, pkloss_n

def reward(beta1, beta2, beta3, bwd, delay, pkloss, cost_action):
    bwd_cost_ = [i* beta1 for i in bwd] #bwd available
    delay_cost_ = [j* beta2 for j in delay] #delay
    pkloss_cost = [k* beta3 for k in pkloss] #pkloss

    rew = [cost_action+i+j+k for i,j,k in zip(bwd_cost_,delay_cost_,pkloss_cost)] #reward/cost of each link
    return rew

def get_dict(data): 
    A_0 = data["node1"].values.tolist() #get nodes 
    Z_0 = data["node2"].values.tolist() #get neighbors
    
    #the order of cost paths is in the same as 'data'
    bwd = data["bwd"].values.tolist() #get cost paths 
    delay = data["delay"].values.tolist()  # get cost paths
    pkloss = data["pkloss"].values.tolist()  # get cost paths

    bwd = list(map(lambda x: round(float(x),6), bwd)) #with 6 decimals
    delay = list(map(lambda x: float(x), delay))
    pkloss = list(map(lambda x: float(x), pkloss))

    bwd_n, delay_n, pkloss_n = normalize_path_cost(bwd, delay, pkloss)
    
    #weigths for reward
    beta1=1
    beta2=1
    beta3=1
    cost_action = 1

    weight_=reward(beta1,beta2,beta3,bwd_n,delay_n,pkloss_n,cost_action)
    A = A_0 + Z_0 
    Z = Z_0 + A_0
    weight_ = weight_ + weight_

    #turns all values in A and Z integers
    A = list(map(lambda x:int(x), A)) #takes values in list, aplies lambda and return the result into A
    Z = list(map(lambda x:int(x), Z))
    
    A_key = sorted(set(A))
    links={}
    
    for i in range(len(A_key)):
        links[A_key[i]] = []
    
    for i in range(len(A)):
        if Z[i] not in links[A[i]]:
            links[A[i]].append(Z[i])

    mydict = links
    with open('/home/controlador/ryu/ryu/app/SDNapps_proac/neighbors.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in mydict.items():
           writer.writerow([key, value])

    return {"A":A,
           "Z":Z,
           "weight": weight_,
           "links":links}