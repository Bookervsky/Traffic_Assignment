from Construct_Network import read_net, read_OD
import Frank_Wolfe as FW
import time
import pandas as pd

'''
IMPORTRANTE NOTE:
You may have noticed that the number of nodes exceeds the number of zones in the Network and maybe confused that,
if the given OD demand are between zones rather than nodes, how do we assgin traffic among nodes since their
numbers don't match?

Well, in the *_node.tntp file, zones are represented as (centroid)nodes in order to perform traffic assignment.
As we know, traffic demand only goes from zones to zones, so those centroids are actually the origins and destinations
of traffic demand. The traffic and only start or end from centroids and cannot pass through them.

As you'll see on the third line of the *_net.tntp file :  "<FIRST THRU NODE> : 39", this indicates volume can only pass 
through nodes from the 39th node onwards, which implies the first (39-1) nodes are centroids representing traffic zones.

So, when calculating route distances, you start from a centroid, pass through nodes, and finnaly end at another centroid.
'''

def traffic_assignment(nodeSet,linkSet,zoneSet,ODSet,loading,accuracy,maxIter):

    gap = float('inf')
    s_k = {link:0.0 for link in linkSet} # initial flow distribution

    iter = 0
    start_time = time.time()
    while gap > accuracy:
        # 1. # update gradient and Direction-finding subproblem
        if loading == 'deterministic':
            SP_cost, s_k = FW.direction_finding_subproblem(nodeSet,linkSet,zoneSet,ODSet)
        elif loading == 'stochastic':
            pass
        # 2. # find step size
        step_size = FW.find_step_size(linkSet,s_k) # find step size using frank-wolfe.
        # 3. # update solution(flow) and cost
        update(linkSet,step_size,s_k)
        # 4. calculate convergence
        gap = calculate_gap(linkSet,SP_cost)

        iter += 1
        if iter > maxIter:
            print("The assignment did not converge with the desired gap and max iterations are reached")
            print("current gap ", gap)
            break
    print("Assignment took", time.time() - start_time, " seconds")
    print("assignment converged in ", iter, " iterations")

def update(linkSet,step_size,s_k):
    '''
    Update the cost of each link based on the flow.
    For now the cost only considers the travel time.
    Link generalized cost = Link travel time + toll_factor * toll + distance_factor * distance
    '''
    for l in linkSet:
        link = linkSet[l]
        link.flow = link.flow + step_size * (s_k[l] - link.flow)
        link.cost = link.free_flow_time * (1 + link.b * (link.flow / link.capacity) ** link.power) #BPR function
    return

def calculate_gap(linkSet,SP_cost):
    '''
    Calculate the gap between the current and previous flow.
    '''
    gap = 0.0
    new_SP_cost = round(sum([linkSet[l].flow * linkSet[l].cost for l in linkSet]),4)
    SP_cost = round(SP_cost,4)
    gap = round(abs((new_SP_cost/SP_cost)-1),4)

    return gap


def output(linkSet):
    rows = []
    for l in linkSet:
        link = linkSet[l]
        rows.append({'init_node':link.init_node,
                            'term_node':link.term_node,
                            'flow':link.flow,
                            'cost':link.cost})
    flow = pd.DataFrame(rows,columns=['init_node','term_node','flow','cost'])
    net = pd.read_csv('SiouxFalls/processed_data/SiouxFalls_net.csv')
    result = net.merge(flow,how='left',on=['init_node','term_node'])
    result.to_csv('SiouxFalls/Results/UE_result.csv',index=False)

    return result



def main():
    nodes_file = 'SiouxFalls/processed_data/SiouxFalls_node.csv'
    net_file = 'SiouxFalls/processed_data/SiouxFalls_net.csv'
    OD_file = 'SiouxFalls/processed_data/OD.omx'
    nodeSet,linkSet = read_net(nodes_file,net_file)
    zoneSet, ODSet = read_OD(OD_file)
    traffic_assignment(nodeSet,linkSet,zoneSet,ODSet,'deterministic',0.001,100)
    output(linkSet)
    return

if __name__ == '__main__':
    main()