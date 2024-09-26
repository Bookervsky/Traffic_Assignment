import math

def likelihood(linkSet,nodeSet):
    '''
    Calculate the likelihood of the link flow. (Dial's algorithm)
    '''
    for link in linkSet:
        if link.feasible:
            link.log_likelihood = math.exp(nodeSet[link.init_node].dist - nodeSet[link.term_node].dist - link.cost)
    return