from Q_routing import Q_routing
from get_all_routes import get_best_nodes, get_best_net, get_all_best_routes, get_cost, count_routes, get_route
from collections import Counter

def get_result(R,Q,alpha,epsilon,n_episodes,start,end):
    Q, epsilon = Q_routing(R,Q,alpha,epsilon,n_episodes,start,end)
    nodes = get_best_nodes(Q,start,end) #get best nodes to reach dest
    graph = get_best_net(Q,nodes) #get dict with the path for the best nodes
    route_len = len(get_route(Q,start,end)) #calculate number of nodes in best route
    routes = get_all_best_routes(graph,start,end,route_len+1)
    result = count_routes(routes)
    
    ends_find = []
    for i in range(len(routes)):
        ends_find.append(routes[i][-1])
    ends_find = list(set(ends_find)) 

    cost = []
    for i in routes:
        cost.append(get_cost(R,i))
    Counter(cost)
    res = {"nodes":nodes,
            "graph":graph,
            "final_Q": Q,
            "ends_find":ends_find,
            "cost":dict(Counter(cost)),
            "routes_number":result['routes_number'],
            "all_routes":result['all_routes']}
    return res