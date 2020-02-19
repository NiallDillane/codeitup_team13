from flask import Flask
import pandas as pd
from typing import List, Tuple
from Passenger import Passenger
from Stop import Stop
from Bus import Bus
from flask_cors import CORS

import random
app = Flask(__name__)
cors = CORS(app)

availableStops = pd.read_csv('data/stops.txt')
usedStops = pd.DataFrame()
routes = List[Tuple[List[Stop], List[Bus]]]  # ((stop1, stop2, stop3), bus1, bus2)


@app.route('/', methods=["GET"])
def startGame():
    return 'game started'

@app.route('/joetest')
def test():
    stop1 = Stop(5)
    stop2 = Stop(4)
    stop3 = Stop(3)
    stop4 = Stop(1)
    stop1.tempAddAdj(stop2)
    stop1.tempAddAdj(stop3)
    stop2.tempAddAdj(stop1)
    stop2.tempAddAdj(stop3)
    stop3.tempAddAdj(stop1)
    stop3.tempAddAdj(stop2)
    stop4.tempAddAdj(stop3)
    route = (stop1,stop2,stop3)
    graph = gengraph(route)
    print(graph.get(stop1))
    return "go away"
    #find_path(graph, stop1, stop4)

@app.route('/hi')
def endGame():
    return 'game ended'

def generatePassengers(stop):
    # random point
    # TODO may want to go back to itself, just remove stop from the possible route
    endStop = random.choice(random.choice(stop.routes))
    # start with stop and find route to endStop, each stop has variable adjacent
    
    #passenger = Passenger(stop,route)
    #Generates passenger, uncomment when route is set
    return 0


# @app.route('/loadCSV')
# def loadCSV():
#     global availableStops
#     availableStops = pd.read_csv('data/stops.txt')

@app.route('/generateStop')
def generateStop():
    global availableStops
    global usedStops

    _stop = availableStops.sample(n=1)
    usedStops = usedStops.append(_stop)
    availableStops = availableStops.drop(_stop.index)
    
    lati = str(_stop.stop_lat.values[0])
    longi = str(_stop.stop_lon.values[0])
    return lati + ' , ' + longi # because long is a keyword don't get mad at me

def gengraph(route):
    graph = dict()
    for stop in route:
        print ("setting" + graph[stop] + " as key")
        graph[stop] = stop.adjacent
        print (" and " + stop.adjecnt + " as value")
    return graph

def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None
