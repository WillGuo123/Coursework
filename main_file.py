import networkx as nx
import random as r
import matplotlib.pyplot as plt
import numpy as np
import supporting_lib_1 as f
from itertools import combinations
import supporting_lib_2 as g

# NOTE ON THE USER INTERFACE: THE TABULAR I/O DISPLAYED IN THE REPORT WILL BE IMPLEMENTED NEXT TERM;
# THE INPUT-TABLE TO GRAPH CONVERSION AND THE ALGORITHM'S VECTOR OUTPUT TO OUTPUT-TABLE CONVERSION ARE
# TRIVIAL; BUT THOUGHT IT BEST TO DECIDE ON MORE SPECIFIC HARDWARES FIRST


# INPUTS TO TWEAK (N IS THE THE LIST OF NODES; E IS THE LIST OF EDGES)
N = [[0,5], [1,5], [2,5], [3,4], [4,2], [5,1], [6,1], [7,1], [8,1], [9,1], [10,5], [11,3], [12,4], [13,5], [14,2], [15,3]]
E = [[(0,2), 10], [(1,2), 15], [(3,5), 17], [(2,4), 12], [(1,3),11], [(0,6), 30], [(7,2), 1], [(7,6),3], [(9,1),3], [(8,6),7], [(2,8),5], [(9,1),3], [(9,10),7], [(11,1),3], [(10,11),3], [(2,12),3], [(3,13),7], [(14,5),9], [(1,15),13], [(15,12),2], [(11,14),3]]


# PARAMETERS. THESE DON'T NEED TUNING FOR NOW
T = 10**25
rate = 0.90
epoch = 10000


Path, Cost = f.ShortestPath(N, E, T, rate, epoch, display = True)
print('Final Route: ',Path)
print('Final Total Time: ', Cost)
plt.show()
