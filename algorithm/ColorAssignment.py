# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec

def ColorAssignment():
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, _, bio_flag = utils.loadData(s, settings)
        MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge.txt", s)
        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)


ColorAssignment()