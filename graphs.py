import networkx
from queue import PriorityQueue
import graphviz

class Graph:
    def __init__(self, start=None):
        self._adjlist = {}
        self._valuelist = {}
        if start is not None:
            for edge in start:
                a, b = edge
                self.add_edge(a, b)

    def __len__(self):
        return len(self._adjlist.keys())

    def add_edge(self, a, b):
        if a not in self._adjlist:
            self._adjlist[a] = set()
        self._adjlist[a].add(b)
        if b not in self._adjlist:
            self._adjlist[b] = set()
        self._adjlist[b].add(a)

    def add_vertex(self, v):
        if v not in self._adjlist:
            self._adjlist[v] = set()

    def remove_vertex(self, v):
        if v in self._adjlist:
            del self._adjlist[v]
        for item in self._adjlist:
            if v in self._adjlist[item]:
                self._adjlist[item].remove(v)
        self.edges()

    def remove_edge(self, a, b):
        if a in self._adjlist:
            self._adjlist[a].remove(b)

    def vertices(self):
        return list(self._adjlist.keys())

    def edges(self):
        eds = []
        for a in self._adjlist:
            for b in self._adjlist[a]:
                if (b, a) in eds:
                    continue
                else:
                    eds.append((a, b))
        return eds

    def neighbours(self, v):
        """Give the neighbours of v"""
        return self._adjlist[v]

    def get_vertex_value(self, v):
        return self._valuelist.get(v, None)

    def set_value(self, v, value):
        if v in self.vertices():
            self._valuelist[v] = value

    def __str__(self):
        return str(self._adjlist)

class WeightedGraph(Graph):
    def __init__(self, start=None):
        super().__init__(start)
        self._weightlist = {}

    def get_weight(self, a, b):
        if (a, b) in self._weightlist:
            return self._weightlist.get((a, b), None)
        elif (b, a) in self._weightlist:
            return self._weightlist.get((b, a), None)
        else:
            return

    def set_weight(self, a, b, weight):
        if (a, b) in self.edges():
            self._weightlist[(a, b)] = weight
            self._weightlist[(b, a)] = weight
        if (b, a) in self.edges():
            self._weightlist[(a, b)] = weight
            self._weightlist[(b, a)] = weight

G = WeightedGraph()

# def cost(u, v):
#     return G.get_weight(u, v)

# def costs2attributes(G, cost, attr='weight'):
#     for a, b in G.edges():
#         G[a][b][attr] = cost(a, b)

def dijkstra(g, source, cost=lambda u,v: 1):
    # costs2attributes(G, cost, attr='weight'
    visited_v = []
    pq = PriorityQueue()
    ## count of vertices
    counted_v_dict = {v : None for v in g.vertices() if v != source}
    for v in g.vertices():
        g.set_value(v, float("inf"))
    g.set_value(source, 0)

    pq.put((g.get_vertex_value(source), source))
    ## get the shortest path
    while not pq.empty():
        i, cur_v = pq.get()
        visited_v.append(cur_v)
        for next_v in g.neighbours(cur_v):
            try:
                weight = g.get_weight(cur_v, next_v)
            except:
                weight = cost(cur_v, next_v)
            if next_v not in visited_v:
                old_weight = g.get_vertex_value(next_v)
                new_weight = g.get_vertex_value(cur_v) + weight
                if new_weight < old_weight:
                    g.set_value(next_v, new_weight)
                    pq.put((new_weight, next_v))
                    counted_v_dict[next_v] = cur_v
    ## find shortest path
    shortest_path = {}
    for v in g.vertices():
        if v != source:
            tar = v
            path = []
            while tar != source:
                path.append(tar)
                if v not in counted_v_dict:
                    break
                tar = counted_v_dict[tar]
            path.append(source)
            path.reverse()
            if v not in counted_v_dict:
                path = []
            shortest_path[v] = path
    return shortest_path

gbg_linecolors = {'1':'gray', '2' :'yellow', '3':'blue', '4':'green', '5': 'red', '6':'orange',
                  '7': 'brown', '8': 'purple', '9': 'lightblue', '10':'lightgreen', '11':'black',
                  '13':'pink'}

# def visualize(gragh, view='dot', name='mygraph', nodecolors=None):
#     dot = graphviz.Graph(engine=view)
#
#     for stop in gragh.all_stops():
#         x, y = gragh.stop_position(stop)
#         pos_x, pos_y = str(x), str(y)
#         dot.node(stop, label=stop, shape='rectangle',  fontsize='10pt',pos=pos_x + ',' + pos_y + '!',
#                  width='0.4', height='0.08')
#     for v in gragh.vertices():
#         if str(v) in nodecolors:
#             dot.node(str(v), style='filled', color=nodecolors[str(v)])
#     for line in gragh.all_lines():
#         stops = gragh.line_stops(line)
#         for i in range(len(stops) - 1):
#             dot.edge(stops[i], stops[i + 1], color=gbg_linecolors[str(line)], penwidth=str(2))
#     dot.render( name, view=True)

def visualize(gragh, view='dot', name='mygraph', nodecolors=None):
    dot = graphviz.Graph(engine=view, graph_attr={'size': '12, 12'})
    for v in gragh.vertices():
        if str(v) in nodecolors:
            dot.node(str(v), style='filled', color=nodecolors[str(v)])
        else:
            dot.node(str(v))
    for (a, b) in gragh.edges():
        dot.edge(str(a), str(b))
    dot.render( name, view=True)

def view_shortest(Gra, source, target, cost= lambda u, v :1):
    path = dijkstra(Gra, source, cost)[target]
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(Gra, view='dot', nodecolors=colormap)


# def demo():
#     eds = [('1', '2'), ('1', '3'), ('2', '4'), ('3', '4')]
#     WeightedGraph(eds)
#     # G.add_edge('1', '2')
#     # G.add_edge('1', '3')
#     # G.add_edge('2', '4')
#     # G.add_edge('3', '4')
#     G.set_weight('1', '2', 2)
#     G.set_weight('1', '3', 3)
#     G.set_weight('2', '4', 6)
#     G.set_weight('3', '4', 2)
#     for v in G.vertices():
#         print(G[v])
#     print(dijkstra(G, '1')['4'])
def demo():
    G = Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()
    # test_graph()
    # test_edge()
    # test_shortest_path()
