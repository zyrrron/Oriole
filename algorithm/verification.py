# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import sys
import UpdateFunctions as uf
import csv
import EnlargeCommunity as ec
sys.path.append("../Oriole")
import utils
import time
import networkx as nx
import EdgeFunctions as ef
import CommunityFunctions as ccf
import InOutFunctions as iof
import InitiateFunctions as inf
import CalculationFunctions as clf


# If solution find, we return "verification passed" and save the current clustering solution.
def Verification():
    # Load samples and settings
    samples, settings = utils.loadSettings()
    txt0 = open(f"VerifyFailed.txt", "a")
    txt1 = open(f"VerifyPassedAfterMerge.txt", "a")
    txt2 = open(f"VerifyPassedDirectly.txt", "a")
    ResultFile = open(f"VerifyResult.csv", "a", newline="")
    csvwriter = csv.writer(ResultFile)
    if ResultFile.tell() == 0:
        csvwriter.writerow(["Benchmark", "Comm before verify", "Comm after verify", "Cell-cell Edges before verify", "Edges after verify"])

    # Verify samples iteratively
    for s in samples:
        begin_time = time.time()

        # Load data and check if we can directly put all the nodes in one community
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep, timestep2, \
            bio_flag, height, DAG, height2, attempts, ub = utils.loadData(s, settings)
        CellEdgeBeforeVerify, CommBeforeVerify = G_primitive.number_of_edges(), G_primitive.number_of_nodes()

        # If the max size for one community is bigger than the current total number of the nodes, output it and continue the next sample
        if len(G_primitive.nodes) < S_bounds[1]:
            CostTime = time.time() - begin_time
            txt2.write(f"{s},")
            csvwriter.writerow([s, CommBeforeVerify, 1, CellEdgeBeforeVerify, 0])
            iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}_{constraint[0]}.txt', G_primitive, [], CostTime)
            print("All nodes can be put in one community!")
            continue

        # Initiate communities
        CurrentVerifyResult = inf.createInitialCommunities(G_primitive)

        # Find the pending community, if no pending community, save current cluster result.
        PendingCommunities = ccf.findPendingCommunities(G_primitive, CurrentVerifyResult, constraint, bio_flag)
        if len(PendingCommunities) == 0:
            CostTime = time.time() - begin_time
            txt2.write(f"{s},")
            csvwriter.writerow([s, CommBeforeVerify, CommBeforeVerify, CellEdgeBeforeVerify, CellEdgeBeforeVerify])
            iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}_{constraint[0]}.txt', G_primitive, CurrentVerifyResult, CostTime)
            continue
        print("PendingCommunities: ", PendingCommunities)

        # Start to solve the pending communities
        # Find the worst case in the PendingCommunities
        PendingCommunity = ccf.findWorstCommunity(G_primitive, PendingCommunities, CurrentVerifyResult, bio_flag)
        print("PendingCommunity: ", PendingCommunity)

        # Start to solve the worst case by enlarging its size
        VerifyResult, VerifyFlag, ErrorLog, _ = ec.enlargeCommunity(G_primitive, PendingCommunity, S_bounds, ConstraintType, timestep,
                                                       constraint, loop_free, priority, CurrentVerifyResult, bio_flag, ub, height)

        # If VerifyFlag is false, that means the graph and constraints don't pass the verification, user should change
        # it later. If it is ture, save the result. Then we go to the merging stage.
        if VerifyFlag:
            print("Verification passed!")
            txt1.write(f"{s},")
            CellToCellEdges = clf.calculateCellEdges(G_primitive, VerifyResult)
            csvwriter.writerow([s, CommBeforeVerify, len(uf.mapCommunityToNodes(VerifyResult)), CellEdgeBeforeVerify, CellToCellEdges])
            # Write current verify solution into a output file
            CostTime = time.time() - begin_time
            iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}_{constraint[0]}.txt', G_primitive, VerifyResult, CostTime)
        else:
            txt0.write(f"{s}\n")
            iof.reportIssue(out_path, ErrorLog)


Verification()
