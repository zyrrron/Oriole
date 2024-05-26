import utils
import EdgeFunctions as ef
import collections


def findIOEdges():

    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Check samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, out_path, timestep, timestep2, \
        bio_flag, height, DAG, height2, attempt_range, ub, _, _, _, _ = utils.loadData(s, settings)
        in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(DAG)
        different_edges = ef.findIOEdges(G_primitive, DAG)
        D = collections.defaultdict(list)

        # Add input edges and output edges into D
        for edge in different_edges:
            if edge[0] in in_nodes:
                D["input"].append(edge)
            else:
                D["output"].append(edge)

        # Sort the two list
        D["input"].sort()
        D["output"].sort()

        # Write it into a file
        with open(f"{out_path}/IOEdgeInfo.txt", "w") as file:
            for row in D:
                for edge in D[row]:
                    file.write(f"{row}, {edge}\n")
                    print(f"{row}, {edge}")


findIOEdges()