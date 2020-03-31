import random
from get_all_routes import get_best_nodes
import numpy as np

def update_Q(T,Q,current_state, next_state, alpha):
    current_t = T[current_state][next_state]
    current_q = Q[current_state][next_state]
    
    #updating SARSA
    # best_next_action_val = min(Q[next_state].values())
    # for action in Q[next_state].keys():
    #     if Q[next_state][action] ==  best_next_action_val:
    #         best_next_action = action
    # # print(best_next_action)
    # new_q = current_q + alpha * (current_t + gamma * Q[next_state][best_next_action] - current_q) #for each state, it will choose the minimun furture cost instead of maximum future reward SARSA

    #updating Q-learning
    new_q = current_q + alpha * (current_t + min(Q[next_state].values()) - current_q) #for each state,
                                #it will choose the minimun furture cost instead of maximum future reward.
    Q[current_state][next_state] = new_q
    return Q

def get_key_of_min_value(dic):
        min_val = min(dic.values())
        return [k for k, v in dic.items() if v == min_val]

def Q_routing(T,Q,alpha,epsilon,n_episodes,start,end): #Fill Q table and explore all options
    #--------------e-greedy decay---------------------------------
    # min_epsilon = 0.01
    # max_epsilon = 0.9
    # decay_rate = 0.001
    episode_hops = {}

    #T is network info
    for e in range(1,n_episodes+1):
        # print("Episode {0}:".format(e))
        current_state = start
        goal = False
        stored_states = []

        while not goal:
            #takes the next hops negihbors for state
            valid_moves = list(Q[current_state].keys())
            
            if len(valid_moves) <= 1:
                next_state = valid_moves[0]
            else:
                best_action = random.choice(get_key_of_min_value(Q[current_state]))
                if random.random() < epsilon:
                    next_state = best_action
                else:
                    valid_moves.pop(valid_moves.index(best_action))
                    next_state = random.choice(valid_moves)
            Q = update_Q(T,Q,current_state, next_state, alpha)
            current_state = next_state
            # print(next_state)
            stored_states.append(next_state)

            if next_state in end:
                goal = True
        #     print('Q-table:', Q)
        #     print('Switches', stored_states)
        #     episode_hops[e] = stored_states
        # print('resume',episode_hops)
        # name = '~/ryu/ryu/SDNapps_proac/RoutingGeant/stretch/Graphs_parameters/alpha_'+str(alpha)+'/'+str(it)+'_alpha_'+str(alpha)+'_epsilon_'+str(epsilon)+'_'

        # with open(str(name)+'hops_episodes.json', 'w') as json_file:
        #     json.dump(episode_hops, json_file, indent=1)
        
        #--------------e-greedy decay---------------------------------
        # e += 1
        # epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*e)
        # print epsilon
    return Q, epsilon
