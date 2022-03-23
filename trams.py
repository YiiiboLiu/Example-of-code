import sys
import json
import graphviz
import math
import graphs as G

class TramStop:
    def __init__(self, name, lines=[],lat = 0, lon = 0 ):
        self._lines = lines
        self._name = str(name)
        self._position = (float(lon), float(lat))

    def add_line(self, line):
        line = str(line)
        if line not in self._lines:
            return self._lines.append(line)

    def get_lines(self):
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position(float(lat), float(lon))


class TramLine:
    def __init__(self, num, stops=[]):
        self._number = str(num)
        self._stops = stops

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


class TramNetwork(G.WeightedGraph, TramStop, TramLine):
    def __init__(self, lines, stops, times):
        super().__init__()
        self._linedict = {}
        if lines:
            for line in lines:
                self._linedict[line] = TramLine(line, stops=lines[line])

        self._stopdict = {}
        if stops:
            for s in stops:
                linelist = []
                for line in lines:
                    if s in lines[line]:
                        linelist.append(line)
                if 'lat' in stops[s] and 'lon' in stops[s]:
                    self._stopdict[s] = TramStop(s, lines=linelist, lat=stops[s]['lat'], lon=stops[s]['lon'])
                else:
                    self._stopdict[s] = TramStop(s, lines=linelist)


        self._timedict = {}
        if times:
            self._timedict = times


    def all_stops(self):
        stops_list = []
        for stop in self._stopdict:
            stops_list.append(stop)
        return stops_list

    def all_lines(self):
        lines_list = []
        for line in self._linedict:
            lines_list.append(line)
        return lines_list

    def extreme_positions(self):
        stops = self._stopdict.values()
        minlat = min([s._position[0] for s in stops])
        maxlat = max([s._position[0] for s in stops])
        minlon = min([s._position[1] for s in stops])
        maxlon = max([s._position[1] for s in stops])
        return minlon, minlat, maxlon, maxlat

    def geo_distance(self, a, b):
        lat1 = math.radians(float(self._stopdict[a].get_position()[0]))
        lat2 = math.radians(float(self._stopdict[b].get_position()[0]))
        lon1 = math.radians(float(self._stopdict[a].get_position()[1]))
        lon2 = math.radians(float(self._stopdict[b].get_position()[1]))
        dlat = lat1 - lat2
        dlon = lon1 - lon2
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        distance = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
        distance = round(distance / 1000, 6)
        return distance

    def line_stops(self, line):
        return self._linedict[line].get_stops()

    # def remove_lines(self, lines):

    def stop_lines(self, a):
        return self._stopdict[a].get_lines()

    def stop_position(self, a):
        return self._stopdict[a].get_position()

    def transition_time(self, a, b):
        if b in self._timedict[a]:
            return self._timedict[a][b]
        else:
            return self._timedict[b][a]

def json2data(FILE):
    with open(FILE, 'r', encoding='UTF-8') as f:
        return json.load(f)

def readTramNetwork(tramfile='tramnetwork.json',geo=False):
    f = json2data(tramfile)
    g = TramNetwork(f['lines'], f['stops'], f['times'])
    if not geo:
        for stop in g._stopdict:
            g.add_vertex(stop)
        for line in g._linedict:
            for i in range(len(g._linedict[line].get_stops()) - 1):
                u = g._linedict[line].get_stops()[i]
                v = g._linedict[line].get_stops()[i + 1]
                g.add_edge(u, v)
                if v in g._timedict[u]:
                    g.set_weight(u, v, g._timedict[u][v])
                else:
                    g.set_weight(u, v, g._timedict[v][u])
        return g
    else:
        for stop in g._stopdict:
            g.add_vertex(stop)
        for line in g._linedict:
            for i in range(len(g._linedict[line].get_stops()) - 1):
                u = g._linedict[line].get_stops()[i]
                v = g._linedict[line].get_stops()[i + 1]
                g.add_edge(u, v)
                g.set_weight(u, v, g.geo_distance(u, v))
        return g




def scaled_position(network):
    # compute the scale of the map
    minlat, minlon, maxlat, maxlon = network.extreme_positions()
    size_x = maxlon - minlon
    scalefactor = len(network) / 4  # heuristic
    x_factor = scalefactor / size_x
    size_y = maxlat - minlat
    y_factor = scalefactor / size_y

    return lambda xy: (x_factor * (xy[0] - minlon), y_factor * (xy[1] - minlat))


gbg_linecolors = {'1':'gray', '2' :'yellow', '3':'blue', '4':'green', '5': 'red', '6':'orange',
                  '7': 'brown', '8': 'purple', '9': 'lightblue', '10':'lightgreen', '11':'black',
                  '13':'pink'}

def demo():
    g = readTramNetwork(geo=True)
    a, b = input('from,to ').split(',')
    G.view_shortest(g, a, b)

def network_graphviz(network, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size':'12, 12'})

    for stop in network.all_stops():
        x, y = network.stop_position(stop)
        if positions:
            x, y = positions(network)((x, y))
        pos_x, pos_y = str(x), str(y)
        print(network.extreme_positions())

        dot.node(stop, label=stop, shape= 'rectangle', fontsize='10pt', pos=pos_x + ',' + pos_y + '!',
                 width='0.4', height='0.08')
    for line in network.all_lines():
        stops = network.line_stops(line)
        for i in range(len(stops)-1):
            dot.edge(stops[i], stops[i+1],color=gbg_linecolors[str(line)],penwidth=str(2))
    dot.render(view=True)


if __name__ == '__main__':
    demo()
    # network = readTramNetwork()
    # network_graphviz(network)

