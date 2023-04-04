import InOutFunctions as iof
import UpdateFunctions as uf
import EnlargeCommunity as ec
import utils
import os

def Merge():
    # Load samples and settings
    samples, settings = utils.loadSettings()
    res = {}

    # Verify samples iteratively
    for s in samples:
        for upperbound in range(120, 131):
            cell = 1

            # Load verification result
            G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, timestep, bio_flag = utils.loadData(s, settings)
            S_bounds[1] = upperbound
            VerifyResult = iof.loadSolution(f"{out_path}/sol_after_verify.txt", s)
            CommunityNumToNodes = uf.mapCommunityToNodes(VerifyResult)

            # Start merging from the community with the least incoming or outgoing edges.
            MergeResult, MergeFlag, MergeErrorLog = ec.enlargeCommunityMerge(G_primitive, S_bounds, ConstraintType,
                                constraint, loop_free, priority, timestep, VerifyResult, target_n, bio_flag)

            if MergeFlag:
                # Write current merge solution into a output file
                iof.writeSolution(out_path, f'/sol_after_merge_{upperbound}.txt', G_primitive, MergeResult)
            else:
                iof.reportMergeIssue(G_primitive, out_path, MergeResult, MergeErrorLog, timestep, VerifyResult)

            res[upperbound] = len(uf.mapCommunityToNodes(MergeResult))
            outfile = out_path + "/plot_data.txt"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            f_out = open(outfile, 'w')
            for key in res:
                f_out.write(f"{key}\t{res[key]}\n")
            print(upperbound, res[upperbound])
Merge()