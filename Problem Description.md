# Traffic Assignment Problem Formulation
The Traffic Assignment Problem under User equilibrium can be formulated as :  
  
$$\displaystyle
\min \sum_a \int_{0}^{v_a} t_a(x) \ dx
$$  
s.t.  
$$\displaystyle v_a = \sum_{i} \sum_{j} \sum_{r} \alpha_{ij}^{ar}x_{ij}^{r}$$  
$$\displaystyle \sum_{r}x_{ij}^{r} = T_{ij}$$  
$$\displaystyle \sum_{r}x_{ij}^{r} = T_{ij}$$  
$$\displaystyle v_a \geq 0, x_{ij}^{r} \geq 0$$  

in which,   
$\displaystyle v_a$ denotes volume on link $a$
$\displaystyle t_{a}(x)$ denotes travel time on link $a$, which is normally defined as the BPR function
$\displaystyle x_{ij}^{r}$ denotes volume on path r from origin i to destination j.
$\displaystyle \alpha_{ij}^{ar}$ denotes whether link a is on route from $i$ to $j$  
### Category of math problem to which it belongs
The objective is continuous and non-linear. The decision variable $\displaystyle x_{ij}^{r}$ denotes the volume on path a from $i$ to $j$ in physical world and the feasible set it composes possesses attributes below:
1. Boundedness. The volume can only be a real number which is no less than 0 and no bigger than the demand from O to D.
2. Closedness. The volume is continuous. 
3. Convexity. The affine combination of any two solutions is still in the feasible set.  
Hence, it is a non-linear optimization problem whose feasible set is compact and convex.  

The Frank-Wolfe Alogrithm offers a solution for such kind of problem.

# Frank-Wolfe Algorithm
Assume we are unfamiliar with non-linear optimization and have no idea how to solve it. Under similiar circumstances, the possible ideas are finding similarities between the unkown and known. So we may come up with that is it possible we turn it into a linear optimization so it could be solved in polynominal time? The answer is yes, that's excatly what the Frank-Wolfe Algorithm does.  
  
The core idea of Frank-Wolfe Algorithm is to solve the linear approximation of the problem given by the first-order **Taylor approximation**, which means, we transform a non-linear optimization $\displaystyle \min f(x)$ into $\min \nabla f(x_k) + \nabla f(x_k)(x-x_k)$, since $x_k$ is a constant, the problem is further tranformed into $\displaystyle \min \nabla f(x_k)x$ 

The step of Frank-Wolfe Algorithm would be:
1. Set a initial feasible solution $x_k$
2. **Direction-finding subproblem:** $\displaystyle \min \nabla f(x_k)x$, the solution is denoted as $s_k$
3. **Step Size detemination:** $\displaystyle \min f(x_{k}+\alpha(s_k-x_k))$, in which $\displaystyle 0 \leq \alpha \leq 1$.
4. **Update:** let $\displaystyle x_{k+1} = x_{k}+\alpha(s_k-x_k)$
5. Exit if the convergence condition is satisfied.

# Solving Traffic Assignment problem using Frank-Wolfe Algorithm
In the context of traffic assignment problem, the objective is $\displaystyle \min \sum_a \int_{0}^{v_a} t_a(x) \ dx$, hence:  
The **Direction-finding subproblem** would be: $\displaystyle \min \sum_a t_a(x_k)x$, and the solution of Direction-finding subproblem would be s_k.  
The **Step Size detemination** would be: $\displaystyle \min f(x + stepsize * (s_k - x))$. Since $\displaystyle f(x)$ is a convex and bounded function(which can be proved by $\displaystyle f''(x) \geq 0$, just to remind that $\displaystyle f'(x)$ is the BPR function), it reaches its global minimum point at its local minimum point, which is when: $\displaystyle (s_k - x)f'(x) = 0$, which is:  
$\displaystyle (s_k - x) * t_a(x + stepsize * (s_k - x)) = 0$