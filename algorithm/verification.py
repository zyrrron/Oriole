# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import sys
import os
sys.path.append("../Oriole")
import utils
import networkx as nx
import EdgeFunctions as ef
import CheckConstraintFunctions as ccf
import InOutFunctions as iof
import InitiateFunctions as inf
import collections


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




# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, PendingCommunities, S_bounds, ConstraintType, constraint, loop_free, priority):
    # create the sub-network centering with the pending community
    SubNetwork = inf.createSubNetwork()
    pass


# If no solution find, return current best clustering solution, and the return the community caused the problem.
def reportIssue():
    pass


# Save current verification solution and send it to "merging.py"
def saveSolution():
    pass


# If solution find, we return "verification passed" and save the current clustering solution.
def main():
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load data and check if we can directly put all the nodes in one community
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep = utils.loadData(s, settings)

        # If the max size for one community is bigger than the current total number of the nodes, output it and continue the next sample
        if len(G_primitive.nodes) < S_bounds[1]:
            iof.writeVerifySolution(out_path, G_primitive, [])
            continue

        # Initiate communities
        CurrentVerifyResult = inf.createInitialCommunities(G_primitive)

        CurrentStep = 1
        while CurrentStep < timestep:

            # Find the pending community, if no pending community, save current cluster result.
            PendingCommunities = findPendingCommunities(G_primitive, CurrentVerifyResult, constraint)
            if len(PendingCommunities) == 0:
                iof.writeVerifySolution(out_path, G_primitive, CurrentVerifyResult)
                break

            # Start to solve the pending communities
            enlargeCommunity(G_primitive, PendingCommunities, S_bounds, ConstraintType, constraint, loop_free, priority)

            CurrentStep += 1


main()

