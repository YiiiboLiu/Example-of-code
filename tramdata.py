## dictionary function


import json
import math



def data2json(data, FILE):
    with open(FILE, 'w+', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

def json2data(FILE):
    with open(FILE, 'r', encoding='UTF-8') as f:
        return json.load(f)

def read_file(FILE):
    with open(FILE, 'r', encoding='UTF-8') as f:
        return [line.replace('\n', '') for line in f.readlines()]

#stop dictionary
def build_tram_stops(jsonobject):
    stopdicts = {}
    for stop in jsonobject:
        stopdic = {}
        stopdic['lat'] = jsonobject[stop]["position"][0]
        stopdic['lon'] = jsonobject[stop]["position"][1]
        stopdicts[stop] = stopdic
    return stopdicts

#lines dictionary
def build_tram_lines(file):
    linelists = {}
    linelist = []
    for item in file:
        if item[-1:] == ':':
            linelist = []
            linelists[item[:-1]] = linelist
        elif item == '':
            continue
        else:
            linelist.append(item[:-5].rstrip())
    return linelists

#time dictionary
def build_tram_time(file):
    linelists = {}
    linelist = {}
    time_lists = {}
    time_list = {}
    for item in file:
        if item[-1:] == ':':
            linelist = {}
            linelists[item[:-1]] = linelist
        elif item == '':
            continue
        else:
            linelist[item[:-5].rstrip()] = item[-2:]
    for line in list(linelists.keys()):
        stoplist = list(linelists[line].keys())
        for stop in range(len(stoplist)-1):
            for check_line in list(linelists.keys()):
                check_stoplist = list(linelists[check_line].keys())
                for check_stop in range(len(check_stoplist)-1):
                    if check_stoplist[check_stop] == stoplist[stop]:
                        time_list[check_stoplist[check_stop+1]] = abs(int(linelists[check_line][check_stoplist[check_stop+1]]) - int(linelists[check_line][check_stoplist[check_stop]]))
            time_lists[stoplist[stop]] = time_list
            time_list = {}

    for start in list(time_lists.keys()):
        for end in list(time_lists.keys()):
            if start in time_lists[end] and end in time_lists[start]:
                del[time_lists[start][end]]

    # if time_lists[a].keys == b:
    return time_lists

def build_tram_network(file1, file2):
    lists = {}
    lists["stops"] = build_tram_stops(file1)
    lists["lines"] = build_tram_lines(file2)
    lists["times"] = build_tram_time(file2)
    data2json(lists, 'tramnetwork.json')
    return lists

#  [line, line ]
def lines_via_stop(lines_dict, stop):
    line_stop = []
    for item in lines_dict.keys():
        for key in lines_dict[item]:
            if stop == key:
                line_stop.append(item)
    return line_stop

def lines_between_stops(lines_dict, stop1, stop2):
    final_lines = []
    lines = lines_dict.keys()
    for line in lines:
        if stop1 in lines_dict[line] and stop2 in lines_dict[line]:
            final_lines.append(line)
    if final_lines:
        return final_lines


def time_between_stops(lines_dict,time_dict, line, stop1, stop2):
    total_time = 0
    if stop1 in lines_dict[line] and stop2 in lines_dict[line]:
        for i in range(len(lines_dict[line])):
            if stop1 == lines_dict[line][i]:
                start = i
            if stop2 == lines_dict[line][i]:
                end = i
        if start < end:
            while start < end:
                time = time_dict[lines_dict[line][start]][lines_dict[line][start + 1]]
                start += 1
                total_time = total_time + time
        if start > end:
            while start > end:
                time = time_dict[lines_dict[line][end]][lines_dict[line][end + 1]]
                end += 1
                total_time = total_time + time
    else:
        print("stop are not on this line!")
    return total_time

def distance_between_stops(distance_dict, stop1, stop2):
    #in radians
    lat1 = math.radians(float(distance_dict[stop1]['lat']))
    lat2 = math.radians(float(distance_dict[stop2]['lat']))
    lon1 = math.radians(float(distance_dict[stop1]['lon']))
    lon2 = math.radians(float(distance_dict[stop2]['lon']))
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    distance = 2 * math.asin(math.sqrt(a)) * 6371 * 1000
    distance = round(distance / 1000, 6)
    return distance

# def distance(distance_dict, stop1, stop2):
#     a = (float(distance_dict[stop1]['lat']), float(distance_dict[stop1]['lon']))
#     b = (float(distance_dict[stop2]['lat']), float(distance_dict[stop2]['lon']))
#     return h.haversine(a, b)


def answer_query(tramdict, query):
    q = query
    f = tramdict
    if 'via' in q:
        stop = q[q.index('via') + 3:].strip()
        for c in f['lines']:
            if stop in f['lines'][c]:
                return print(lines_via_stop(f['lines'], stop))
        print("unknown arguments")
        return
    elif 'between' in q and 'and' in q:
        stop1 = q[q.index('between') + 7: q.index('and')].strip()
        stop2 = q[q.index('and') + 3:].strip()
        for c in f['lines']:
            if stop1 in f['lines'][c] and stop2 in f['lines'][c]:
                return print(lines_between_stops(f['lines'], stop1, stop2))
        if stop1 in f['stops'] and stop2 in f['stops']:
            return
        print("unknown arguments")
        return
    elif 'time with' in q and 'from' in q and ' to ' in q:
        line = q[q.index('with') + 4: q.index('from')].strip()
        stop1 = q[q.index('from') + 4: q.index(' to ')].strip()
        stop2 = q[q.index(' to ') + 3:].strip()
        for c in f['lines']:
            if stop1 in f['lines'][c] and stop2 in f['lines'][c]:
                return print(time_between_stops(f['lines'], f['times'], line, stop1, stop2))
        if stop1 in f['stops'] and stop2 in f['stops']:
            return
        print("unknown arguments")
        return
    elif 'distance from ' in q and ' to ' in q:
        stop1 = q[q.index('from') + 4: q.index(' to ')].strip()
        stop2 = q[q.index(' to ') + 4:].strip()
        for c in f['lines']:
            if stop1 in f['lines'][c] and stop2 in f['lines'][c]:
                return print(distance_between_stops(f['stops'], stop1, stop2))
        if stop1 in f['stops'] and stop2 in f['stops']:
            return
        print("unknown arguments")
        return
    else:
        print('sorry, try again')


def dialogue(jsonfile):
    tramdict = json2data(jsonfile)
    query = input('>')
    while query != 'quit':
        answer_query(tramdict, query)
        query = input('>')

jsonobject = json2data('tramstops.json')
tram_lines = read_file('tramlines.txt')
tramdict = json2data('tramnetwork.json')
jsonfile = 'tramnetwork.json'
distance_dict = build_tram_stops(jsonobject)
lines_dict = build_tram_lines(tram_lines)
time_dict = build_tram_time(tram_lines)

print(tram_lines)

# if __name__ == "__main__":
#     if 'init' in sys.argv:
#         build_tram_network(jsonobject,tram_lines)
#     else:
#         dialogue(jsonfile)


