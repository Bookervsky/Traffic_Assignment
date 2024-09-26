import openmatrix as omx
from Network_class import Node, Link, Zone

def read_OD(OD_file): # Read _trips.tntp and return OD pairs, trip pairs
    zoneSet, ODSet = {}, {}
    file = omx.open_file(OD_file,'r')
    OD_matrix = file['matrix']
    for i in range(1,len(OD_matrix)+1): # i and j represent origin and destination zones, respectively
        if i not in zoneSet:
            zoneSet[i] = Zone([i])
        for j in range(1,len(OD_matrix[i-1])+1):
            ODSet[(i,j)] = OD_matrix[i-1][j-1]
            if j not in zoneSet:
                zoneSet[j] = Zone([j])
            if j not in zoneSet[i].destList:
                zoneSet[i].destList.append(j)
    file.close()
    return zoneSet, ODSet


def read_net(nodes_file,net_file):
    nodeSet, linkSet = {}, {}    
    with open (nodes_file, 'r') as file:
        header = file.readline().strip().split(',')
        for line in file:
            parts = line.strip().split(',')
            nodeSet[int(parts[0])] = Node(parts)

    with open (net_file, 'r') as file:
        header = file.readline().strip().split(',')
        for line in file:
            parts = line.strip().split(',')
            linkSet[(int(parts[0]),int(parts[1]))] = Link(parts)
            if int(parts[1]) not in nodeSet[int(parts[0])].outlinks:
                nodeSet[int(parts[0])].outlinks.append(int(parts[1]))
            if int(parts[0]) not in nodeSet[int(parts[1])].inlinks:
                nodeSet[int(parts[1])].inlinks.append(int(parts[0]))

    return nodeSet, linkSet



    