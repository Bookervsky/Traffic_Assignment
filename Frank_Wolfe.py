from Shortest_Path import Dijkstra, tracePreds
import scipy.optimize as opt
import numpy as np

def direction_finding_subproblem(nodeSet,linkSet,zoneSet,ODSet):
    '''
    This is actually the All or Nothing assignment result, and let's see why:
    The dirction-finding linear subproblem is formulated as :    
                                                            min<s_k,∇f(x_k)>
    in which s_k is the solution of the subproblem, and ∇f(x_k) is the gradient at x_k, which is known.
    In the context of traffic assignment, the derivative of the objective function is the BPR function, which is
    formulated as t_a(x_a), in which x_a is the flow on link a.
    Therefore, the subproblem is formulated as:
                                                            min<s_k,t_a(x_a)>
    whose physical meaning is to find the route that minimizes the total travel cost given the current flow distribution,
    and that is right the physical meaning of  All or Nothing assignment result. 
    (We also know that the subproblem is a convex linear minimum problem, who has only one solution, so that's it.)
    '''
    Auxiliary_Flow = {link:0 for link in linkSet}
    SP_cost = 0.0 # Total Shortest path cost. All trips are assigned to the shortest path.
    Origin_zones = [zoneSet[i].zoneid for i in zoneSet]
    for Origin in Origin_zones:
        Dijkstra(Origin,nodeSet,linkSet)
        for Dest in zoneSet[Origin].destList:
            try:
                demand = ODSet[(Origin,Dest)]
            except KeyError:
                demand = 0
            SP_cost += nodeSet[Dest].dist * demand # Multiply demand becasue SP_cost represent total cost of all travelers.
            if Origin == Dest:
                continue
            for link in tracePreds(Dest,nodeSet):
                Auxiliary_Flow[link] += demand
    s_k = Auxiliary_Flow
    return SP_cost, s_k

def find_step_size(linkSet,s_k):
    '''
    To find step_size that 
    Min: f(x_k + step_size * (s_k - x_k))
    in which x_k is the current flow, s_k is dirction-finding subproblem solution.

    Since f(x) is convex in the context of traffic assignment (this is because f''(x) > 0), and a 
    convex function reaches its minimum when f'(x) == 0.  In traffic assginment problem,  f'(x) is BPR function, so
    f'(step_size) == (s_k - x_k) * BPR(x_k + step_size * (s_k - x_k))

    Therefore, the step_size value that minimizes f(x) is the solution to the equation:
    (s_k - x_k) * BPR(x_k + step_size * (s_k - x_k)) == 0.
    '''

    def step_size(step_size): # step size for the Frank-Wolfe algorithm
        sum_derivative = 0.0 # The derivative of the objective function should be t_a(x_a), in which x_a is flow on link a. 
        for l in linkSet:
            link = linkSet[l]
            x = link.flow
            new_x = x + step_size * (s_k[l] - x)
            BPR_new_x = link.free_flow_time * (1 + link.b * (new_x / link.capacity) ** link.power)
            sum_derivative += (s_k[l] - x) * BPR_new_x
        return sum_derivative
    
    sol = opt.fsolve(step_size,np.array([0.05]))
    return max(0.1,min(1,sol[0]))
