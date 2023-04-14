# After verification stage, we will work on the solution optimization
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec
import CommunityFunctions as ccf


def Merge():
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load verification result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, timestep, bio_flag, height, DAG = utils.loadData(s, settings)
        VerifyResult = iof.loadSolution(f"{out_path}/sol_after_verify.txt", s)
        CommunityNumToNodes = uf.mapCommunityToNodes(VerifyResult)

        # If the number of current communities is smaller than target number, return.
        if len(CommunityNumToNodes) < target_n:
            print("Verification solution is good enough according to the target number of communities!")
            continue

        # If the number of target n can never achieve because S_bound[1] is too small, return error
        if S_bounds[1] * target_n < len(G_primitive.nodes()):
            print("The upper bound of one community make it impossible to get target_n communities to take all the nodes in this graph!")
            continue

        # If S_bound[1] is big enough to take all the nodes in one community
        if S_bounds[1] >= len(G_primitive.nodes):
            iof.writeSolution(out_path, '/sol_after_merge.txt', G_primitive, [])
            print("All nodes can be put in one community!")
            continue

        # Start merging from the community with the least incoming or outgoing edges.
        print("Now try merging the communities!")
        attempts = 10
        MergeResult, MergeFlag, MergeErrorLog = ec.enlargeCommunityMerge(G_primitive, S_bounds, ConstraintType,
                            constraint, loop_free, priority, timestep, VerifyResult, target_n, bio_flag, height, attempts)

        if MergeFlag:
            print("Merge passed according to the target N!")

            # Write current merge solution into an output file
            iof.writeSolution(out_path, '/sol_after_merge.txt', G_primitive, MergeResult)
        else:
            MergeResult = merge_final_check(G_primitive, S_bounds, MergeResult)
            iof.reportMergeIssue(G_primitive, out_path, '/sol_after_merge.txt', MergeResult, MergeErrorLog, timestep, VerifyResult)


def merge_final_check(G, S_bounds, MergeResult):
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    maxCommLen, maxComm = 0, ''
    for tmp in CommunityNumToNodes:
        if len(CommunityNumToNodes[tmp]) > maxCommLen:
            maxCommLen = len(CommunityNumToNodes[tmp])
            maxComm = tmp

    if len(G.nodes) - S_bounds[1] <= maxCommLen:
        for node in MergeResult:
            if MergeResult[node] != maxComm:
                MergeResult[node] = maxComm + "1"
    return MergeResult


# Merge()