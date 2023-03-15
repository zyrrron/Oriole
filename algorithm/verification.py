# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import sys
sys.path.append("../Oriole")
import utils
import networkx as nx
import EdgeFunctions as ef
import CheckConstraintFunctions as ccf


# Find the communities that cannot meet all constraints, if there is no pending community exists, return -1, else return its community number
def findPendingCommunities(G, result, constraint):
    PendingCommunities = {}
    for key in result:
        res = ccf.checkInOut(G, key, constraint)
        if res != 0:
            PendingCommunities[key] = res
    print(PendingCommunities)
    return PendingCommunities


# Find all neighbor nodes round the given node in G.
def findAllNeighbors(node, G):
    return nx.all_neighbors(G, node)


# put each node in a graph into a distinct community
# each node says: I am my own community
def createInitialCommunities(G):
    d = {}
    for ele in G.nodes:
        d[ele] = ele
    return d



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


# If solution find, we return "verification passed" and save the current clustering solution.
def main():
    # load samples and settings
    samples, settings = utils.loadSettings()

    # verify samples iteratively
    for s in samples:

        # load data
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path = utils.loadData(s, settings)

        # initiate communities
        CurrentClusterResult = createInitialCommunities(G_primitive)

        #
        PendingCommunities = findPendingCommunities(G_primitive, CurrentClusterResult, constraint)

main()

