import UpdateFunctions as uf
import merging as MG
import sys
import math
import os
import EnlargeCommunity as ec
sys.path.append("../Oriole")
import utils
import time
import networkx as nx
import EdgeFunctions as ef
import CommunityFunctions as ccf
import InOutFunctions as iof
import InitiateFunctions as inf
import copy
import csv
import EdgeColoring as ca


def VerifyAndMerge():
    # Load samples and settings
    samples, settings = utils.loadSettings()
    out_path = ""
    ress = []

    # Verify samples iteratively
    for s in samples:
        res = []
        begin_time = time.time()

        # Run and load verification result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep1, timestep2, bio_flag, height, \
        DAG, height2, attempt_range, ub = utils.loadData(s, settings)
        attempt_range_original = copy.deepcopy(attempt_range)
        target_n = math.ceil(len(G_primitive.nodes) / S_bounds[1])
        print(f"Current max gate per cell is {S_bounds[1]}")
        # If the max size for one community is bigger than the current total number of the nodes, output it and continue the next sample
        if len(G_primitive.nodes) < S_bounds[1]:
            CostTime = time.time() - begin_time
            iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}.txt', G_primitive, [], CostTime)
            print("All nodes can be put in one community!")
            continue

        # Start to merge in different max channels for cell-cell communication
        urange = [constraint[0]]

        for upperbound in urange:
            print(f"Current max cell-cell channels for a cell: {upperbound}")
            constraint[0] = upperbound

            # Initiate communities
            CurrentVerifyResult = inf.createInitialCommunities(G_primitive)

            # Find the pending community, if no pending community, save current cluster result.
            PendingCommunities = ccf.findPendingCommunities(G_primitive, CurrentVerifyResult, constraint, bio_flag)
            if len(PendingCommunities) == 0:
                print("No issue with current nodes, verification passed!")
                VerifyResult = CurrentVerifyResult
                CostTime = time.time() - begin_time
                iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}_{upperbound}.txt', G_primitive, CurrentVerifyResult, CostTime)
            else:
                print("PendingCommunities: ", PendingCommunities)

                # Start to solve the pending communities
                # Find the worst case in the PendingCommunities
                PendingCommunity = ccf.findWorstCommunity(G_primitive, PendingCommunities, CurrentVerifyResult, bio_flag)
                print("PendingCommunity: ", PendingCommunity)

                # Start to solve the worst case by enlarging its size
                VerifyResult, VerifyFlag, ErrorLog, _ = ec.enlargeCommunity(G_primitive, PendingCommunity, S_bounds, ConstraintType, timestep1,
                                                                         constraint, loop_free, priority, CurrentVerifyResult, bio_flag, ub, height)

                # If VerifyFlag is false, that means the graph and constraints don't pass the verification, user should change
                # it later. If it is ture, save the result. Then we go to the merging stage.
                if VerifyFlag:
                    print("Verification passed!")

                    # Write current verify solution into a output file
                    CostTime = time.time() - begin_time
                    iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}_{upperbound}.txt', G_primitive, VerifyResult, CostTime)
                else:
                    iof.reportIssue(out_path, ErrorLog, f"_{S_bounds[1]}_{upperbound}")
                    continue

            # Set color list, merge+edge coloring time start
            begin_time = time.time()
            ColorOptions = ["black", "gray"]
            for i in range(upperbound):
                ColorOptions.append(f"color{i}")

            # If S_bound[1] is big enough to take all the nodes in one community
            if S_bounds[1] >= len(G_primitive.nodes):
                CostTime = time.time() - begin_time
                iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_{attempt_range_original}.txt', G_primitive, [], CostTime)
                res.append(1)
                print("All nodes can be put in one community!")
                print(upperbound, 1)
                print()

            else:
                # Start merging from the community with the least incoming or outgoing edges.
                # Try different searching order may find more optimal solution and get rid of the local optimal
                # height2 is used for combining the un-neighbored gates, stop in a limited searching height.
                height2 = 3
                CurrentVerifyResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_verify_{S_bounds[1]}_{constraint[0]}.txt", s)
                print(f"Check {attempt_range} attempt range. Now start merging!")
                MergeResult, MergeFlag, MergeErrorLog, ColorFlag, DAG_new = ec.enlargeCommunityMerge_chris(G_primitive, S_bounds, out_path,
                                    constraint, loop_free, timestep2, CurrentVerifyResult, target_n, bio_flag, height, height2, DAG, ColorOptions, attempt_range, ub)

                # Check if the new result is better than the previous one with bigger intercellular constraint
                # if not, don't save it and go to the next one
                # if len(res) > 0 and res[-1] != 'inf' and len(collections.Counter(list(MergeResult.values()))) >= res[-1]:
                #     continue
                if MergeFlag:

                    # Write current merge solution into an output file
                    CostTime = time.time() - begin_time
                    iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_{attempt_range_original}.txt', G_primitive, MergeResult, CostTime)
                    iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_colored.txt', DAG_new)
                else:
                    MergeResult, flag = MG.merge_final_check(G_primitive, S_bounds, MergeResult, loop_free, constraint, bio_flag)
                    if flag:
                        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
                        ColorFlag, DAG_new, _, _ = ca.ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions, 5000)
                    if ColorFlag:
                        CostTime = time.time() - begin_time
                        iof.reportMergeIssue(G_primitive, out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_{attempt_range_original}.txt', MergeResult, MergeErrorLog, attempt_range_original, VerifyResult, target_n, CostTime, f"_{S_bounds[1]}_{upperbound}")
                        iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_colored.txt', DAG_new)

                if ColorFlag:
                    res.append(len(uf.mapCommunityToNodes(MergeResult)))
                else:
                    res.append('inf')
            if target_n == res[-1]:
                print("Target Achieved!")
        ress.append(res)

    # Save the result into a csv file
    outfile = "../results/bionetwork/chris_group/chris_new_requirement/" + "/plot_data.csv"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(outfile, 'w') as f:
        csv_w = csv.writer(f)
        csv_head = [x for x in range(1, 6)]
        csv_w.writerow(csv_head)
        for i in range(len(ress)):
            data_r = [i+1] + ress[i]
            csv_w.writerow(data_r)

    print()


# VerifyAndMerge()