# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.

def ColorAssignment():
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load verification result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, timestep, bio_flag = utils.loadData(s, settings)
        VerifyResult = iof.loadVerifySolution(out_path, s)
        CommunityNumToNodes = uf.mapCommunityToNodes(VerifyResult)


ColorAssignment()