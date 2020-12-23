import networkx as nx
import random as r
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import supporting_lib_2 as g

def Graph(nodes, edges):
    dict = {}
    motivation = 1

    G = nx.Graph()

    for node in nodes:
        G.add_node(node[0])
        G.nodes[node[0]]['points'] = node[1]

    T = []

    for edge in edges:
        G.add_edge(edge[0][0], edge[0][1])
        time = edge[1]
        dict[edge[0]] = time
        T.append(time)
        # G[edge[0]][edge[1]]['weight'] = ((T[-1] + motivation)/(G.nodes[edge[1]]['points']*importance))
        G[edge[0][0]][edge[0][1]]['weight'] = T[-1]

    # print(T)
    G.add_nodes_from(G.nodes())
    return G, dict

# returns a tuple with vector path and cost
def Dijk(G, start, end):
    route = nx.dijkstra_path(G, start, end)
    cost = 0
    for i in range(len(route)-1):
        cost += G[route[i]][route[i+1]]['weight']
    return route, cost

# finds the missing nodes that need to be added for complete subgraph
def toNodeElement(G, S):
    N = []
    for i in S:
        N.append([i, G.nodes[i]['points']])
    return N

# finds the missing edges that need to be added for complete subgraph
def Group(G, E, S, D):
    def MissingEdges(G, S):
        add_edges_list = list(combinations(S,2))
        # print('edges', G.edges)
        # print('edges_list', add_edges_list)
        E_sub = []
        for edge in G.edges:
            if edge in add_edges_list:
                add_edges_list.remove(edge)
                E_sub.append(edge)
            elif (edge[1], edge[0]) in add_edges_list:
                add_edges_list.remove((edge[1], edge[0]))
                E_sub.append((edge[1], edge[0]))
        return add_edges_list, E_sub

    L, E_sub = MissingEdges(G,S)

    E_augment = []
    for i in L:
        D[i] = Dijk(G, i[0], i[1])
        edge_element = [i,D[i][1]]
        E_augment.append(edge_element)

    for i in E_sub:
        E_augment.append([i, G[i[0]][i[1]]['weight']])

    new_E = E_augment
    new_N = toNodeElement(G, S)
    # print(new_N, new_E)
    sub_G, edge = Graph(new_N, new_E)

    return sub_G, edge, D

# Expanded Path
def ExpandedPath(V, D):
    L = [V[0]]
    for i in range(len(V)-1):
        connection = (V[i], V[i+1])
        if connection in D.keys():
            L += D[connection][0][1:]
            # print(D[connection][0])
        elif (V[i+1], V[i]) in D.keys():
            L += D[(V[i+1], V[i])][0][::-1][1:]
            # print(D[(V[i+1], V[i])][0][::-1])
        else:
            L += [V[i], V[i+1]][1:]
            # print([V[i], V[i+1]])
    return L


# The Big Boy--Almost
def Grouped_Trail(G, E, S, D, T,rate, epoch):
    sub_G, edge1, D = Group(G, E, S, D)
    path, cost = g.Sim_Anneal_Optimize(sub_G,T,rate, epoch)
    expanded = ExpandedPath(path, D)
    return path, cost, expanded



# Excluding all travelled from Target
def TargetsLeft(N, S):
    T = [i[0] for i in N]
    for i in S:
        if i in T:
            T.remove(i)
    return T


# Selecting Specific Point Nodes
def NodeSelection(N, p):
    T = []
    for i in N:
        if i[1] == p:
            T.append(i[0])
    return T

def SubPaths(G, N, E, T, rate, epoch, max_p):
    D = {}
    Path = []
    Expanded = []
    Cost = 0
    Target = [i[0] for i in N]

    for i in range(max_p,0,-1):
        # print(i)
        S = NodeSelection(toNodeElement(G, Target), i)
        if len(S) > 1:
            path, cost, expanded = Grouped_Trail(G, E, S, D, T,rate, epoch)
            Target = TargetsLeft(toNodeElement(G, Target), S)
            Path.append(path)
            Expanded.append(expanded)
            Cost += cost
            # print('c', cost)
        elif len(S) == 1:
            Path.append([S[0]])
            Expanded.append([S[0]])
            Cost += 0
            # print('c 0')
        else:
            Path.append([])
            Expanded.append([])
            Cost += 0
            # print('c 0')
    return Path, Cost, Expanded

def Connect(G, Path, Cost, Expanded, Display=True):
    L = []
    if Display:
        print('Groupings by Points from 5 to 1: ', Path)

    while [] in Expanded:
        Expanded.remove([])

    for i in range(len(Expanded)-1):
        connection, cost = Dijk(G, Expanded[i][-1], Expanded[i+1][0])
        L += Expanded[i]
        L += connection[1:-1]
        Cost += cost
    L += Expanded[-1]
    return L, Cost

def ShortestPath(N, E, T, rate, epoch, max_p=5, display = True):
    G, edge = Graph(N, E)
    if display:
        nx.draw(G, pos=nx.circular_layout(G), with_labels=True)
        nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), font_size=8, edge_labels=edge, label_pos=0.2)
    Path, Cost, Expanded = SubPaths(G, N, E, T, rate, epoch, max_p)
    Final_Path, Final_Cost = Connect(G, Path, Cost, Expanded, display)
    return Final_Path, Final_Cost
