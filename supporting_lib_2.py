import networkx as nx
import random as r
import math
import matplotlib.pyplot as plt
import numpy as np

def p(cost0, cost1, T):
    # print(cost1-cost0)
    return max(1/(1+np.e**((cost1-cost0)/T)), 10**-20)

def Path(coords_list):
    path=[]
    for i,j in zip(coords_list[:-1], coords_list[1:]):
        path.append((i,j))
    path.append((coords_list[-1], coords_list[0]))
    return path

def Tot_Dist(path, G):
    dist = 0
    for i,j in path[:-1]:
        if (i,j) in G.edges:
            dist += G[i][j]['weight']
        elif (j,i) in G.edges:
            dist += G[j][i]['weight']
        else:
            dist += 1000
    return dist

def Tot_Point(coords, G):
    points = 0
    for i in coords:
        points += G.nodes[i]['points']
    return points

def Cost(t, p, Time_Limit, strictnness, greed):
    def f(t, Time_Limit, strictnness):
        return strictnness*(np.log(-t+Time_Limit)+np.log(Time_Limit))

    def g(p, greed):
        return greed*p
    return f(t, Time_Limit, strictnness)+g(p, greed)



def Graph(nodes, edges):
    dict = {}
    motivation = 1

    G = nx.Graph()

    for node in nodes:
        G.add_node(node)
        G.nodes[node]['points'] = r.randint(1, 5)

    T = []

    for edge in edges:
        G.add_edge(edge[0][0], edge[0][1])
        time = edge[1]
        dict[edge[0]] = time
        T.append(time)
        # G[edge[0]][edge[1]]['weight'] = ((T[-1] + motivation)/(G.nodes[edge[1]]['points']*importance))
        G[edge[0][0]][edge[0][1]]['weight'] = T[-1]

    G.add_nodes_from(G.nodes())
    return G, dict


def Sim_Anneal_Optimize(G, T0, rate, n, display=True):
    T = T0
    rate = rate
    epoch = n

    current = 0
    nodes_left = [int(i) for i in list(G.nodes)]
    # print(nodes_left)

    coords = nodes_left
    # coords = [current] + r.sample(nodes_left[1:],len(list(G.nodes))-1)
    # print('coords ',coords)
    path = Path(coords)
    # print(path)

    cost0 = Tot_Dist(path, G)
    # print('y', cost0)
    for i in range(epoch):
        x = np.random.uniform()
        # r1, r2, r3, r4 = r.sample(coords,4)
        r1, r2 = r.sample(coords,2)
        r1 = coords.index(r1)
        r2 = coords.index(r2)
        temp1 = coords[r1]
        coords[r1] = coords[r2]
        coords[r2] = temp1

        # temp2 = coords[r3]
        # coords[r3] = coords[r4]
        # coords[r4] = temp2

        # print(coords)
        path = Path(coords)
        cost1 = Tot_Dist(path, G)

        # if display:
        #     print(i, 'cost0 = ', cost0)
        #     print(i, 'cost1 = ', cost1)
        #     print(i, 'x = ', x, ', p = ', p(cost0, cost1, T))

        if x < p(cost0, cost1, T):
            cost0 = cost1
        else:
            temp1 = coords[r1]
            coords[r1] = coords[r2]
            coords[r2] = temp1

            # temp2 = coords[r3]
            # coords[r3] = coords[r4]
            # coords[r4] = temp2

        T = rate*T + 1
    return coords, cost0
