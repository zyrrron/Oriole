import utils
import math
import InOutFunctions as iof
import UpdateFunctions as uf
import collections
import CommunityFunctions as ccf


def countEdgesForEachCell():

    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Check samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, timestep, bio_flag, height, DAG = utils.loadData(
            s, settings)
        MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge.txt", s)
        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
        NumOfSize = collections.defaultdict(int)
        NumOfCommunications = collections.defaultdict(int)

        # record the distribution of cell-cell communication numbers and cell size
        for c in CommunityNumToNodes:
            l = len(CommunityNumToNodes[c])
            NumOfSize[l] += 1
            bio_flag = False
            NumInEdegs = ccf.findIncomingEdgesComm(G_primitive, c, MergeResult, bio_flag)
            NumOutEdegs = ccf.findOutgoingEdgesComm(G_primitive, c, MergeResult, bio_flag)
            NumOfCommunications[len(NumInEdegs)+len(NumOutEdegs)] += 1
            print(c, l, CommunityNumToNodes[c], NumInEdegs, NumOutEdegs)

        print()
        print("Shows the distribution of cells by their total number of gates:")
        print(NumOfSize)

        print()
        print("Shows the distribution of cells by their total number of cell-cell communications excluding input / output:")
        print(NumOfCommunications)




countEdgesForEachCell()