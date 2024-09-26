class Node:
    def __init__(self,_node):
        self.id = int(_node[0])
        self.lat = float(_node[1])
        self.lon = float(_node[2])
        self.inlinks = []
        self.outlinks = []
        self.dist = float('inf') # label is the cost to reach the node in the network(used in Dijkstra)
        self.pred = None # int

class Link():
    def __init__(self,_net):
        self.init_node =int( _net[0])
        self.term_node = int(_net[1])
        self.capacity = float(_net[2])
        self.length = float(_net[3])
        self.free_flow_time = float(_net[4])
        self.b = float(_net[5])
        self.power = int(_net[6])
        self.speed = float(_net[7])
        # self.toll = int(_net[8])
        # self.link_type = int(_net[9])
        self.flow = 0.0
        self.cost = 0.0
        self.feasible = None

class Zone():
    def __init__(self,_zone):
        self.zoneid = _zone[0]
        self.destList = []
