from scipy.optimize import linprog

from itertools import chain, combinations

from graph import Graph

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def linprog_MST_constraints(graph: Graph):
    """
    let E(S) be the set of edges with both endpoints captured by vertex set S.

    Given a graph (V, E):

    x:  vector edge indicator variables
    c:  vector of edge costs

    minimize    c^T x

    subject to  sum(E(V))  = |V| - 1
                    ; Spanning tree has |V|-1 edges

                sum(E(S)) <= |S| - 1    forall subsets S of V
                    ; No subset can be denser than a tree.

                x >= 0
                    ; indicator var should be positive.
    
    This function produces constraint matrices corresponding to this problem.
    """
    graph.order_edges()
    c = graph.cost_order

    ncols = len(graph.edge_order)

    A_eq = [[1]*ncols]  # Single equality constraint for the whole vertex set
    b_eq = [len(graph.vertices)-1]

    A_ub = []
    b_ub = []
    for S in powerset(graph.vertices):
        row = [0]*ncols
        contained_edges = graph.contained_edges(S)
        if len(contained_edges) == 0:
            continue
        for e in contained_edges:
            idx = graph.edge_revmap[e]
            row[idx] = 1
        A_ub.append(row)
        b_ub.append(len(S) - 1)

    print(f"{len(A_ub)} subset constraints.")
    return c, A_ub, b_ub, A_eq, b_eq

def linprog_MST(graph: Graph):
    bounds = (0, None)
    res = linprog(*linprog_MST_constraints(graph), bounds, method="highs-ds")

    sol = res.x
    fval = res.fun
    return sol, fval

if __name__ == "__main__":
    vertices = list(range(4))
    edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (2, 3),
    ]
    costs = [
        1,
        1.1,
        6,
        3,
        5,
    ]
    #costs = [1]*5
    graph = Graph(vertices, edges, costs)
    sol, fval = linprog_MST(graph)
    print(fval, sol)
    for i, v in enumerate(sol):
        v = round(v, 4)
        if v == 1:
            print([graph.edge_order[i]])
