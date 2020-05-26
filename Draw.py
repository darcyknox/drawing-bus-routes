#!/usr/bin/python

import subprocess
import sys
import fileinput
import networkx as nx
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

dictStrings = []
adjLists = {}

for i in fileinput.input():
    pass

filename = fileinput.filename()

p = subprocess.Popen(["java", "BusRoutes", filename], stdout=subprocess.PIPE)
line = p.stdout.readline()

if 'Invalid' in line.decode('utf-8'):
    print(line.decode('utf-8').strip())
    exit()

while (len(line) > 0):
    dictStrings.append(line.decode('utf-8'))
    line = p.stdout.readline()

shortestPathString = dictStrings.pop()

shortestPathRoute = shortestPathString.strip().split("-")

title = shortestPathRoute[0] + " to " + shortestPathRoute[-1]

g = nx.Graph()

# Getting nodes and edges from java output

for string in dictStrings:
    string = string.strip()
    paths = string.split(":")
    a = paths[0]
    g.add_node(a)
    dests = paths[1].split("/")
    if (dests[-1] == ''):
        dests.pop()
    for dest in dests:
        split = dest.split("=")
        b = split[0]
        weight = split[1]
        g.add_node(b)
        g.add_edge(a, b, weight=float(weight))


#print(g.edges())

edgeLabels = nx.get_edge_attributes(g, 'weight')

nodeLabels = {}

# Fruchterman-Reingold method
pos = nx.spring_layout(g)

shortestPathNodes = []
otherNodes = []

for node in g:
    if node in shortestPathRoute:
        shortestPathNodes.append(node)
    else:
        otherNodes.append(node)
    nodeLabels.update({node: node})


nx.draw_networkx_nodes(g, pos, nodelist=shortestPathNodes, node_color='orange', alpha=0.8, node_size=500, with_labels=True)
nx.draw_networkx_nodes(g, pos, nodelist=otherNodes, node_color='blue', alpha=0.5, node_size=500, with_labels=True)

shortestPathEdges = []
otherEdges = []

#print(shortestPathRoute)

for i in range(len(shortestPathRoute) - 1):
    shortestPathEdges.append((shortestPathRoute[i], shortestPathRoute[i + 1]))

for edge in g.edges():
    if edge not in shortestPathEdges and tuple(reversed(edge)) not in shortestPathEdges:
        otherEdges.append(edge)

#print("shortestPathEdges")
#print(shortestPathEdges)

#print("Other edges")
#print(otherEdges)

nx.draw_networkx_edges(g, pos, edgelist=shortestPathEdges, edge_color='green', width=2)
nx.draw_networkx_edges(g, pos, edgelist=otherEdges, edge_color='blue', style='dashed', alpha=0.5, width=2)

nx.draw_networkx_edge_labels(g, pos, edge_labels=edgeLabels)
nx.draw_networkx_labels(g, pos, labels=nodeLabels)
plt.suptitle("COSC326 - Etude 12 - Drawing Bus Routes")
plt.title(title)
plt.margins(0.2)
plt.axis('off')
plt.savefig("BusRoutesGraphic.png")
#plt.show()
