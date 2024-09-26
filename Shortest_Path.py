import heapq
import math
import numpy as np
import scipy.optimize as opt
from Construct_Network import read_net, read_OD

def Dijkstra(origin, nodeSet, linkSet):
    '''
    Calcualtes shortest path from an origin to all other destinations.
    The dist and preds are stored in node instances.
    '''
    for node in nodeSet: # Clear the previous shortest path information.
        nodeSet[node].dist = float('inf')
        nodeSet[node].pred = None
    nodeSet[origin].dist = 0.0
    queue = [(0,origin)] # priority queue to store the shortest path estimate, (dist,node.Node)

    while queue:
        currentnode = nodeSet[heapq.heappop(queue)[1]]
        currentdist = currentnode.dist

        for out_node in currentnode.outlinks:
            link = linkSet[(currentnode.id,out_node)]
            new_node = out_node # int
            pred = currentnode.id
            new_dist = currentdist + link.cost # cost to reach the node
            if new_dist < nodeSet[new_node].dist:
                nodeSet[new_node].dist = new_dist
                nodeSet[new_node].pred = pred
                heapq.heappush(queue,(new_dist,new_node))
    return

def tracePreds(dest, nodeSet):
    '''
    Trace the predecessors of a node to find the shortest path.
    '''    
    tail = nodeSet[dest].pred # start of a link
    head = dest
    route = []
    while tail:
        route.append(((tail,head)))
        head = tail
        tail = nodeSet[tail].pred
    return route

def find_feasible_link(linkSet,nodeSet):

    return



