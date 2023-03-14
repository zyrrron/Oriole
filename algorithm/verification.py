# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import sys
sys.path.append("../Oriole")
import utils


# Store the edge info into a dictionary, use key-value as the direction of an edge.
# We can get new dictionaries after this function, forwardEdge[‘start node’] =‘end node’, backEdge[‘end node’] =‘start node’
def loadData():
    G, G_primitive, DAG = utils.start()
    print(G)
    print(list(G.edges))
    print(list(DAG.edges))
    print(findOutgoingEdges('4', DAG))
    print(findIncomingEdges('4', DAG))
    print(DAG)


# Find the first communities that cannot meet all constraints, if there is no pending community exists, return -1, else return its community number
def findPendingCommunity():
    pass


# Find all incoming edges to node N
def findIncomingEdges(n, DAG):
    return DAG.in_edges(n)


# Find all outgoing edges from node N
def findOutgoingEdges(n, DAG):
    return DAG.edges(n)


# Find all neighbor nodes round the given node in G.
def findNeighbors(node, G):
    return G.neighbors(node)


# put each node in a graph into a distinct community
# each node says: I am my own community
def disctinctEachNode():
    pass


# check community size
def checkSize():
    pass


# check loop in current sub-network
def checkLoop():
    pass


# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity():
    pass


# If no solution find, return current best clustering solution, and the return the community caused the problem.
def reportIssue():
    pass


# Save current verification solution and send it to "merging.py"
def saveSolution():
    pass


# If solution find, we return "verification passed" and pass the solution to the merging stage.
def main():
    loadData()


main()

