# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import copy
import InOutFunctions as iof
import UpdateFunctions as uf
import utils
import EdgeFunctions as ef
import EnlargeCommunity as ec
import collections


# Check next two level neighbor edges from the given one
def PropagandaChecking(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, CellToCellEdges, ColorOptions, bio_flag, depth):

    # max depth is arrived, return back
    if depth <= 0:
        return True

    ComU, ComV = MergeResult[u], MergeResult[v]
    d = {}
    FirstLevelNeighborEdges = ef.findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, bio_flag)
    flag = False

    for uu, vv in FirstLevelNeighborEdges:

        flag = False

        # Check the first level Neighbor Edges one by one.
        ComUU, ComVV = MergeResult[uu], MergeResult[vv]

        # Get the colors of all the neighbor edges.
        NeighborEdges = ef.findNeighborEdges(uu, vv, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, bio_flag)
        NeighborColor = []
        for nu, nv in NeighborEdges:
            NeighborColor.append(CommEdgeColorInfo[MergeResult[nu]][nv])

        # Assign a color for edge (uu, vv)
        for color in ColorOptions:

            # If color is used in a neighbor edge, continue to the next color
            if color in NeighborColor: continue

            # Assign the color to the current edge, update CommEdgeColorInfo
            CommEdgeColorInfo = assignColorForEdge(u, v, CommEdgeColorInfo, ComU, Color)

            # Check one more depth neighbor edges
            if PropagandaChecking(uu, vv, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, CellToCellEdges, ColorOptions, bio_flag, depth-1):
                CommEdgeColorInfo = assignColorForEdge(u, v, CommEdgeColorInfo, ComU, "black")

                # If there is no issue, break the color assignment loop.
                # Otherwise, change the color to the next one (no extra operation to do, because we are in a for loop)
                flag = True
                break

        # No color can be assigned to the edge (uu, vv), break the edge loop and return False
        if not flag: break

    return flag


# Assign the color to the current edge, update CommEdgeColorInfo, go to the next edge
def assignColorForEdge(u, v, CommEdgeColorInfo, ComU, Color):
    CommEdgeColorInfo[ComU][u][v]["Color"] = Color
    CommEdgeColorInfo[ComV][v][u]["Color"] = Color
    return CommEdgeColorInfo


# Find appropriate color for the given edge
def findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag):

    if timestep < 0:
        return CommEdgeColorInfo, False

    if not CellToCellEdges:
        return CommEdgeColorInfo, True

    # Find the tail edge of the current CellToCellEdges list and their terminal nodes, terminal cell
    u, v = CellToCellEdges[-1]
    ComU, ComV = MergeResult[u], MergeResult[v]
    ColorFlag = False

    # Assign a color
    for Color in ColorOptions:

        # Assign the color to the current edge, update CommEdgeColorInfo, go to the next edge
        CommEdgeColorInfo = assignColorForEdge(u, v, CommEdgeColorInfo, ComU, Color)

        # Check if the current color works for the chosen edge (u, v), the depth of recursion in propaganda checking is set to 3
        depth = 2
        if PropagandaChecking(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, CellToCellEdges, ColorOptions[2:], bio_flag, depth):

            # Temporarily remove the edge from CellToCellEdges, if all edges can be colored correctly, it will be an empty list
            # If the color assignment doesn't follow the constraints, we will add the edge back in the first backtracking step
            CellToCellEdges.pop()
            CommEdgeColorInfo, ColorFlag = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, CommEdgeColorInfo,
                                                     CellToCellEdges, timestep - 1, bio_flag)

            # If the current color assignment can give us the solution for the whole graph, return back
            # If the current color cannot be assigned, go backtracking (first backtracking) and try another color until all the colors used
            if ColorFlag:
                break
            else:
                CellToCellEdges.append((u, v))

    # If no color can be assigned to this edge, go backtracking (second backtracking)
    if not ColorFlag:

        # Change back the color for edge (u, v)
        CommEdgeColorInfo = assignColorForEdge(u, v, CommEdgeColorInfo, ComU, "black")

        return CommEdgeColorInfo, False

    # If ColorFlag == True, that means we find the color assignment solution, return to the last level
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
                    D[ComU][u][v] = {"Type": "Outgoing", "Color": "black"}
                else:
                    D[ComU][u] = {v:{"Type": "Outgoing", "Color": "black"}}

                if v in D[ComV]:
                    D[ComV][v][u] = {"Type": "Incoming", "Color": "black"}
                else:
                    D[ComV][v] = {u:{"Type": "Incoming", "Color": "black"}}

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
        CommEdgeColorInfo, ColorFlag = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions[2:], CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag)

        for u,v in DAG.edges:
            Color = "black"

            # If the edge doesn't exist in G_primitive, set it as "black"
            if u in MergeResult and v in MergeResult:

                # If the edge is inside a community, set it "gray"
                if MergeResult[u] == MergeResult[v]:
                    Color = "gray"

                # Otherwise, it is cell-cell edge. change the color for the edge
                else:
                    Color = CommEdgeColorInfo[MergeResult[u]][u][v]["Color"]
            DAG.add_edge(u, v, color=Color)

        if ColorFlag:
            # Write edge list with color
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)
        else:
            print("Cannot find appropriate solution for edge coloring!")
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)


# Assume we have totally 4 different cell-cell communication molecular, set 4 as the input parameter. Then we will give the solution with numbers.
ColorOptions = ["black", "gray", "purple", "blue", "green", "orange"]
ColorAssignment(ColorOptions)

