# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import copy

import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EnlargeCommunity as ec
import collections


# Check next two level neighbor edges from the given one
def PropagondaChecking(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, ColorTmp):
    return True


# Find appropriate color for the given edge
def findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep):

    if timestep < 0:
        return CommEdgeColorInfo, False

    if not CellToCellEdges:
        return CommEdgeColorInfo, True

    G = copy.deepcopy(DAG)

    for u,v in CellToCellEdges:
        ComU, ComV = MergeResult[u], MergeResult[v]
        ColorFlag = False

        for Color in ColorOptions:

            # Check if the current color works for the chosen edge (u, v)
            if PropagondaChecking(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, Color):

                # Assign the color to the current edge, update CommEdgeColorInfo, go to the next edge
                for tmp in CommEdgeColorInfo[ComU][u]:
                    if tmp["Node"] == v:
                        tmp["Color"] = Color
                for tmp in CommEdgeColorInfo[ComV][v]:
                    if tmp["Node"] == u:
                        tmp["Color"] = Color
                # Temporarily remove the edge from CellToCellEdges, if all edges can be colored correctly, it will be a empty list
                # If the color assignment doesn't follow the constraints, we will add the edge back in the first backtracking step
                CellToCellEdges.remove((u, v))
                CommEdgeColorInfo, ColorFlag = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, CommEdgeColorInfo,
                                                         CellToCellEdges, timestep - 1)

                # If the current color cannot be assigned, go backtracking (first backtracking) and try another color
                if ColorFlag:
                    break
                else:
                    CellToCellEdges.append((u, v))
        # If no color can be assigned to this edge, go backtracking (second backtracking)
        if not ColorFlag:
            # Change back the color for edge (u, v)
            for tmp in CommEdgeColorInfo[ComU][u]:
                if tmp["Node"] == v:
                    tmp["Color"] = "black"
            for tmp in CommEdgeColorInfo[ComV][v]:
                if tmp["Node"] == u:
                    tmp["Color"] = "black"

            return CommEdgeColorInfo, False

        # If ColorFlag == True, that means we find the color assignment solution, skip from the loop
        else:
            return CommEdgeColorInfo, True


def createColorInfo(MergeResult, CommunityNumToNodes, G):
    D = collections.defaultdict(dict)
    CellToCellEdges = []
    # Initiate all the primitive edges in ColorInfo as "black"
    for u, v in G.edges:

        # If the edge is a cell-cell edge, set it to black as initiation
        if u in MergeResult and v in MergeResult:
            ComU, ComV = MergeResult[u], MergeResult[v]
            if ComU != ComV:
                CellToCellEdges.append((u, v))

                # If it is the first time to add value to key u or v, create a list and add a dictionary inside
                # If key u or v exists before, append a dictionary to the related value.
                if u in D[ComU]:
                    D[ComU][u].append({"Type": "Outgoing", "Node": v, "Color": "black"})
                else:
                    D[ComU][u] = [{"Type": "Outgoing", "Node": v, "Color": "black"}]

                if v in D[ComV]:
                    D[ComV][v].append({"Type": "Incoming", "Node": u, "Color": "black"})
                else:
                    D[ComV][v] = [{"Type": "Incoming", "Node": u, "Color": "black"}]

    return D, CellToCellEdges

def ColorAssignment(ColorOptions):
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, target_n, _, bio_flag = utils.loadData(s, settings)
        MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge.txt", s)
        DAG = utils.load_graph(settings, s)
        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)

        # Create a dictionary, key is the community number, value is a dictionary.
        # The inner dictionary, key is an edge connecting to the community in the last level, value is its color
        CommEdgeColorInfo, CellToCellEdges = createColorInfo(MergeResult, CommunityNumToNodes, G_primitive)

        # Color the cell-cell edges
        timestep = 1000000
        CommEdgeColorInfo, ColorFlag = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions[2:], CommEdgeColorInfo, CellToCellEdges, timestep)

        for u,v in DAG.edges:
            Color = "black"

            # If the edge doesn't exist in G_primitive, set it as "black"
            if u in MergeResult and v in MergeResult:

                # If the edge is inside a community, set it "gray"
                if MergeResult[u] == MergeResult[v]:
                    Color = "gray"

                # Otherwise, it is cell-cell edge. change the color for the edge
                else:
                    for tmp in CommEdgeColorInfo[MergeResult[u]][u]:
                        if tmp["Node"] == v:
                            Color = tmp["Color"]
            DAG.add_edge(u,v, color=Color)

        if ColorFlag:
            # Write edge list with color
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)
        else:
            print("Cannot find appropriate solution for edge coloring!")
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)


# Assume we have totally 4 different cell-cell communication molecular, set 4 as the input parameter. Then we will give the solution with numbers.
ColorOptions = ["black", "gray", "purple", "blue", "green", "orange"]
ColorAssignment(ColorOptions)

