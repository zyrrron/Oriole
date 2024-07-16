# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

# After verification stage, we will work on the solution optimization
import sys
sys.path.append("../")
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec
import time
import csv
import math
import CalculationFunctions as clf
import copy
import CommunityFunctions as ccf


def Merging():
    # Load samples and settings
    samples, settings = utils.loadSettings()
    ResultFile = open(f"../results/csv_result_collection/MergeResult.csv", "a", newline="")
    csvwriter = csv.writer(ResultFile)
    if ResultFile.tell() == 0:
        csvwriter.writerow(["Benchmark", "Comm before merge", "Comm after merge", "Cell-cell Edges before merge", "Edges after merge"])

    # Verify samples iteratively
    for s in samples:
        begin_time = time.time()

        # Load verification result
        G_primitive, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, _, timestep, \
            bio_flag, color_flag, height, DAG, height2, attempt_range, ub, _, _, _, _ = utils.loadData(s, settings)

        attempt_range_original = copy.deepcopy(attempt_range)
        if target_n == -1:
            target_n = math.ceil(len(G_primitive.nodes) / S_bounds[1])
        VerifyResult, TotalCommOld = iof.loadSolution(f"{out_path}/sol_after_verify_{S_bounds[1]}_{constraint}.txt", s)
        CellToCellEdgesOld = clf.calculateCellEdges(G_primitive, VerifyResult)

        # If the number of current communities is smaller than target number, return.
        if TotalCommOld < target_n:

            csvwriter.writerow([s, TotalCommOld, CellToCellEdgesOld, TotalCommOld, CellToCellEdgesOld])
            print("Verification solution is good enough according to the target number of communities!")
            continue

        # If the number of target n can never achieve because S_bound[1] is too small, return error
        if S_bounds[1] * target_n < len(G_primitive.nodes()):
            print("The upper bound of one community make it impossible to get target_n communities to take all the nodes in this graph!")
            continue

        # If S_bound[1] is big enough to take all the nodes in one community
        if S_bounds[1] >= len(G_primitive.nodes):
            CostTime = time.time() - begin_time
            csvwriter.writerow([s, TotalCommOld, CellToCellEdgesOld, 1, 0])
            iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint}_{attempt_range}.txt', G_primitive, [], CostTime)
            print("All nodes can be put in one community!")
            continue

        # Start merging from the community with the least incoming or outgoing edges.
        print("Now try merging the communities!")

        MergeResult, MergeFlag, MergeErrorLog = ec.enlargeCommunityMerge(G_primitive, S_bounds, out_path,
                            constraint, loop_free, timestep, VerifyResult, target_n, bio_flag, color_flag, height, height2, attempt_range, ub)

        CostTime = time.time() - begin_time
        print(f"Time Cost: {CostTime}")

        # Save merge result comparison table
        CellToCellEdges = clf.calculateCellEdges(G_primitive, MergeResult)
        csvwriter.writerow([s, TotalCommOld, CellToCellEdgesOld, len(uf.mapCommunityToNodes(MergeResult)), CellToCellEdges])

        # Write current merge solution into an output file
        if MergeFlag:
            print(f"Merge passed according to the target N: {target_n}!")
            iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint}_{attempt_range_original}.txt', G_primitive, MergeResult, CostTime)
        else:
            MergeResult_new, flag = merge_final_check(G_primitive, S_bounds, MergeResult, loop_free, constraint, bio_flag)
            if flag:
                print("New merge result after final check!")
                iof.reportMergeIssue(G_primitive, out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint}_{attempt_range_original}.txt', MergeResult_new, MergeErrorLog, attempt_range_original, VerifyResult, target_n, CostTime, f"_{S_bounds[1]}_{constraint[0]}")
            else:
                print("No changes on the merge result after final check!")
                iof.reportMergeIssue(G_primitive, out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint}_{attempt_range_original}.txt', MergeResult, MergeErrorLog, attempt_range_original, VerifyResult, target_n, CostTime, f"_{S_bounds[1]}_{constraint[0]}")


def merge_final_check(G, S_bounds, r, loop_free, constraint, bio_flag):
    MergeResult = copy.deepcopy(r)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    maxCommLen, maxComm = 0, ''
    flag = False
    for tmp in CommunityNumToNodes:
        if len(CommunityNumToNodes[tmp]) > maxCommLen:
            maxCommLen = len(CommunityNumToNodes[tmp])
            maxComm = tmp

    newComm = "0"
    if len(G.nodes) - S_bounds[1] <= maxCommLen:
        for node in MergeResult:
            if MergeResult[node] != maxComm:
                MergeResult[node] = newComm

        # If current merge operation (added one neighbor community to current one in the last level) can be accepted,
        # update the current merge result to MergeResult and break the loop, go to the next merge community.
        # checkloop = 0 and checkInOutComm = 0 means the current community meets all the constraints
        if ((loop_free and ccf.checkLoopComm(G, newComm, MergeResult, bio_flag) == 0) or not loop_free) and \
                ccf.checkInOutComm(G, newComm, constraint, MergeResult, bio_flag) == 0:
            flag = True
    return MergeResult, flag


# Merging()