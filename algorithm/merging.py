# After verification stage, we will work on the solution optimization
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec


# Load samples and settings
samples, settings = utils.loadSettings()

# Verify samples iteratively
for s in samples:

    # Load verification result
    G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, timestep = utils.loadData(s, settings)
    VerifyResult = iof.loadVerifySolution(out_path, s)
    CommunityNumToNodes = uf.mapCommunityToNodes(VerifyResult)

    # If the number of current communities is smaller than target number, return.
    if len(CommunityNumToNodes) < target_n:
        print("Verification solution is good enough according to the target number of communities!")
        continue

    # Start merging from the community '1'
    MergeResult, MergeFlag, MergeErrorLog = ec.enlargeCommunityMerge(G_primitive, '1', S_bounds, ConstraintType,
                        constraint, loop_free, priority, timestep, VerifyResult, target_n)

