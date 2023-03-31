# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec
import collections


# Find appropriate color for the given edge
def findColor(ColorNum, ColorUsedInEachCommunity, ComU, ComV):


    return Color


def ColorAssignment(ColorNum):
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, _, bio_flag = utils.loadData(s, settings)
        MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge.txt", s)
        DAG = utils.load_graph(settings, s)
        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
        ColorUsedInEachCommunity = collections.defaultdict(dict)

        for u,v in DAG.edges:
            Color = "black"

            # If the edge doesn't exist in G_primitive, Sign it as "black"
            if u in MergeResult and v in MergeResult:

                # If the edge is inside a community, set it "gray"
                if MergeResult[u] == MergeResult[v]:
                    print(u, v, "gray")
                    Color = "gray"

                # If not, change it into the color founded by findColor()
                else:
                    Color = findColor(ColorNum, ColorUsedInEachCommunity, MergeResult[u], MergeResult[v])

                    # Data structure: ColorUsedInEachCommunity = {"1":{"input":{"3":{"color":"red", "OutsideNode": "4"}}, "output":{...}}, ...}
                    if MergeResult[u] in ColorUsedInEachCommunity:


            G_primitive.add_edge(u,v, weight=Color)



# Assume we have totally 4 different cell-cell communication molecular, set 4 as the input parameter. Then we will give the solution with numbers.
ColorAssignment(4)

