import UpdateFunctions as uf
import merging as MG
import sys
import math
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

        # Run and load verification result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep1, timestep2, bio_flag, height, DAG = utils.loadData(
            s, settings)
        target_n = math.ceil(len(G_primitive.nodes) / S_bounds[1])
        print(f"Current max gate per cell is {S_bounds[1]}")
        # If the max size for one community is bigger than the current total number of the nodes, output it and continue the next sample
        if len(G_primitive.nodes) < S_bounds[1]:
            iof.writeSolution(out_path, f'/sol_after_verify_{S_bounds[1]}.txt', G_primitive, [])
            print("All nodes can be put in one community!")
            continue

        # Initiate communities
        VerifyResult = inf.createInitialCommunities(G_primitive)

        # Start to merge in different max channels for cell-cell communication
        for upperbound in range(4, 6):
            constraint[0] = upperbound
            ColorOptions = ["black", "gray"]
            for i in range(upperbound):
                ColorOptions.append(f"color{i}")
            print(f"Current max cell-cell channels for a cell: {upperbound}")

            # If S_bound[1] is big enough to take all the nodes in one community
            if S_bounds[1] >= len(G_primitive.nodes):
                iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}.txt', G_primitive, [])
                res.append(1)
                print("All nodes can be put in one community!")
                print(upperbound, 1)
                print()
            else:

                # Start merging from the community with the least incoming or outgoing edges.
                # Try different searching order may find more optimal solution and get rid of the local optimal
                attempts = 130
                MergeResult, MergeFlag, MergeErrorLog, ColorFlag, DAG_new = ec.enlargeCommunityMerge_chris(G_primitive, S_bounds,
                                    constraint, loop_free, timestep2, VerifyResult, target_n, bio_flag, height, DAG, ColorOptions, attempts)

                if MergeFlag:
                    # Write current merge solution into an output file
                    iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}.txt', G_primitive, MergeResult)
                    iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_colored.txt', DAG_new)
                else:
                    MergeResult, flag = MG.merge_final_check(G_primitive, S_bounds, MergeResult)
                    # if flag:
                    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
                    ColorFlag, DAG_new = ca.ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions)
                    if ColorFlag:
                        iof.reportMergeIssue(G_primitive, out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}.txt', MergeResult, MergeErrorLog, timestep2, VerifyResult, target_n)
                        iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{upperbound}_colored.txt', DAG_new)
                if ColorFlag:
                    res.append(len(uf.mapCommunityToNodes(MergeResult)))
                else:
                    res.append('inf')

    # Save the result into a csv file
    outfile = out_path + "/plot_data.csv"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(outfile, 'w') as f:
        csv_w = csv.writer(f)
        csv_head = [x for x in range(1, 6)]
        csv_w.writerow(csv_head)
        for i in range(len(ress)):
            data_r = [i] + ress[i]
            csv_w.writerow(data_r)

    print()


VerifyAndMerge()