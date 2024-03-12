
class Graph:
    def __init__(self, vertices, edges, costs):
        self.vertices = set(vertices)
        self.edges = {v: set() for v in vertices}
        self.costs = {}
        for edge, cost in zip(edges, costs):
            self.add_edge(edge, cost)

        self._edge_dirty = True
        self.edge_order = None
        self.edge_revmap = None
        self.cost_order = None

    def add_edge(self, edge, cost):
        s, t = edge
        self.edges[s].add(t)
        self.edges[t].add(s)
        self.costs[(t, s)] = cost
        self.costs[(s, t)] = cost
        self._edge_dirty = True

    def remove_edge(self, edge):
        s, t = edge
        self.edges[s].remove(t)
        self.edges[t].remove(s)
        del self.costs[(t, s)]
        del self.costs[(s, t)]
        self._edge_dirty = True

    def remove_vertex(self, v):
        self.vertices.remove(v)
        for s, t in self.edges[v]:
            self.edges[t].remove(s)
            del self.costs[(t, s)]
            del self.costs[(s, t)]
        del self.edges[v]
        self._edge_dirty = True

    def order_edges(self):
        """
        Construct an ordering of this graph's edges.

        For things like throwing it into a matrix
        """
        if not self._edge_dirty:
            return

        self.edge_order = []
        self.edge_revmap = dict()
        self.cost_order = []
        for v in self.vertices:
            for t in self.edges[v]:
                if t > v:
                    e = (v, t)
                    self.edge_revmap[e] = len(self.edge_order)
                    self.edge_revmap[(t, v)] = len(self.edge_order)
                    self.edge_order.append(e)
                    self.cost_order.append(self.costs[e])
        self._edge_dirty = False

    def contained_edges(self, vertex_set):
        """
        Return the edges "fully contained" by the given set of vertices.
        """
        self.order_edges()

        _vertex_it = vertex_set
        vertex_set = set(vertex_set)
        ret = []
        for v in _vertex_it:
            for t in self.edges[v]:
                if t > v and t in vertex_set:
                    ret.append((v, t))

        return ret
