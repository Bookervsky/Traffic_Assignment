import numpy as np
import pandas as pd
import openmatrix as omx

def prepare_nodes(nodefile): # Return nodes as a pandas dataframe
    nodes = pd.read_csv(nodefile, sep='\t')
    nodes.columns = [s.strip() for s in nodes.columns]
    nodes.drop([';'],axis=1,inplace=True)
    dtype = {
        'Node': int,
        'X': float,
        'Y': float
    }
    nodes = nodes.astype(dtype)
    nodes.to_csv('SiouxFalls/processed_data/SiouxFalls_node.csv', index=False)

    return

def prepare_net(netfile): # Return network a pandas dataframe
    net = pd.read_csv(netfile, sep='\t', skiprows=8)
    net.columns = [s.strip().lower() for s in net.columns]
    net.drop(['~',';'],axis=1,inplace=True)
    dtype = {
        'init_node': int,
        'term_node': int,
        'capacity': float,
        'length': float,
        'free_flow_time': float,
        'b': float,
        'power': int,
        'speed': float,
        'toll': float,
        'link_type': int
    }
    net = net.astype(dtype)
    net.to_csv('SiouxFalls/processed_data/SiouxFalls_net.csv', index=False)

    return

def prepare_OD_matrix(OD_file):
    f = open(OD_file, 'r')
    all_rows = f.read()
    blocks = all_rows.split('Origin')[1:] # split OD_file into blocks using 'Origin' as delimiter
    matrix = {} # Initializes an empty dictionary to hold the parsed O-D data.
    for k in range(len(blocks)):
        orig = blocks[k].split('\n')
        dests = orig[1:] #Stores the destination lines
        orig=int(orig[0]) #Converts the first line of the block to an integer, representing the origin zone.

        d = [eval('{'+a.replace(';',',').replace(' ','') +'}') for a in dests]
        destinations = {}
        for i in d:
            destinations = {**destinations, **i}
        matrix[orig] = destinations
    zones = max(matrix.keys())
    mat = np.zeros((zones, zones))
    for i in range(zones):
        for j in range(zones):
            # We map values to a index i-1, as Numpy is base 0
            mat[i, j] = matrix.get(i+1,{}).get(j+1,0)

    index = np.arange(zones) + 1

    myfile = omx.open_file('SiouxFalls/processed_data/OD.omx','w')
    myfile['matrix'] = mat
    myfile.create_mapping('taz', index)
    myfile.close()

    return


nodes_file = 'SiouxFalls/SiouxFalls_node.tntp'
net_file = 'SiouxFalls/SiouxFalls_net.tntp'
OD_file = 'SiouxFalls/SiouxFalls_trips.tntp'
prepare_nodes(nodes_file)
prepare_net(net_file)
prepare_OD_matrix(OD_file)