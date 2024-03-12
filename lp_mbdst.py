from scipy.optimize import linprog

from graph import Graph
from lp_mst import linprog_MST_constraints

def linprog_MBDST(graph: Graph, degree_bounds):
    """
    Bounded Degree Minimum Spanning Tree linear programming relaxation.

    Not guaranteed an integral solution!

    From LP-MST, add a constraint for each vertex that ensures its degree is within
    some specified bound (constrain sum of the edge indicators incident to it)
    """

    c, A_ub, b_ub, A_eq, b_eq = linprog_MST_constraints(graph)

    ncols = len(graph.edge_order)

    # Add degree bound constraints.
    for v in graph.vertices:
        row = [0]*ncols
        for t in graph.edges[v]:
            idx = graph.edge_revmap[(v, t)]
            row[idx] = 1
        A_ub.append(row)
        b_ub.append(degree_bounds[v])

    bounds = (0, None)
    res = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, method="highs-ds")

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
    degree_bounds = [1, 3, 3, 3]
    graph = Graph(vertices, edges, costs)
    sol, fval = linprog_MBDST(graph, degree_bounds)
    print(fval, sol)
