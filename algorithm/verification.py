# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import sys
import os
import EnlargeCommunity as ec
sys.path.append("../Oriole")
import utils
import networkx as nx
import EdgeFunctions as ef
import CommunityFunctions as ccf
import InOutFunctions as iof
import InitiateFunctions as inf
import collections


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

        # Find the pending community, if no pending community, save current cluster result.
        PendingCommunities = ccf.findPendingCommunities(G_primitive, CurrentVerifyResult, constraint)
        if len(PendingCommunities) == 0:
            iof.writeVerifySolution(out_path, G_primitive, CurrentVerifyResult)
            break

        # Start to solve the pending communities
        # Find the worst case in the PendingCommunities
        PendingCommunity = ccf.findWorstCommunity(G_primitive, PendingCommunities, CurrentVerifyResult)
        print(PendingCommunity)

        # PendingCommunities_sorted is an ascendant list, worst case is the last one element.
        ec.enlargeCommunity(G_primitive, PendingCommunity, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, CurrentVerifyResult, 1)


main()

