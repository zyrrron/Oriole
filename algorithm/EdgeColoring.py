# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import copy
import InOutFunctions as iof
import UpdateFunctions as uf
import math
import utils
import EdgeFunctions as ef
import collections


def checkNeighborColor(u, v, CenterColor, NeighborEdges, ColorInfo, MergeResult, bio_flag):

    # scan all the neighbor edges of the center edge
    for uu, vv in NeighborEdges:
        ComUU, ComVV = MergeResult[uu], MergeResult[vv]
        if ColorInfo[ComUU][uu][vv]["Color"] != "black":
            # Because this neighbor edge has color, we don't need to do anything. Its color must have been checked before, then assigned.
            # Thus, we can return false and try another color for the last-level edge.
            if ColorInfo[ComUU][uu][vv]["Color"] == CenterColor and uu != u:
                return False
    return True

# Get the colors of all the neighbor edges for (u,v).
# Check the Neighbor Edges one by one.
# Constraint 1: neighbor edges can share the same color if they are from the same node.
# Constraint 2: neighbor edges cannot share the same color unless they are from the same node.
# Constraint 3: edges can share the same color if they are not neighbor edges.
# Step 1: If the edge is colored and use the same with the given checking edge, then return False
# Step 2: If the edge is not colored, choose one color from currently optional color domain.
# Recursive version
def PropagandaChecking_recursive(u, v, MergeResult, CommunityNumToNodes, ColorInfo, ColorOptions, bio_flag, depth, SearchEdge):

    # max depth is arrived, return back
    # max number of edges we want to check in this
    if depth <= 0 or SearchEdge <= 0:
        return True, SearchEdge

    # find current center edge's color and check its neighbors, see if this edge's color can meet all constraints.
    CenterColor = ColorInfo[MergeResult[u]][u][v]["Color"]
    NeighborEdges = ef.findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, ColorInfo, bio_flag)
    NewColorInfo = copy.deepcopy(ColorInfo)

    # Check if the center edge is colored without breaking any constraint.
    if not checkNeighborColor(u, v, CenterColor, NeighborEdges, NewColorInfo, MergeResult, bio_flag):
        return False, SearchEdge

    # Step 1 has been checked before this function call, in line 67
    # Step 2: If the edge is not colored, choose one color from currently optional color domain.
    for uu, vv in NeighborEdges:
        # check if we searched enough edges.
        if SearchEdge <= 0:
            return True, 0
        SearchEdge -= 1
        # If there is an edge cannot be assigned to any color, flag = false, and return it
        flag = False
        ComUU, ComVV = MergeResult[uu], MergeResult[vv]

        # For the edges has colors, we have checked it in the first if statement checkNeighborColor()
        # Since it passed that statement, we can skip the checking for the un-colored edges here.
        # Here is more complex, because we need to think about which color can be assigned to this neighbor edge.
        if ColorInfo[ComUU][uu][vv]["Color"] == "black":
            Colors = []
            if bio_flag == 1 and uu == u:
                Colors.append(CenterColor)
            else:
                Colors = copy.deepcopy(ColorOptions)
                Colors.remove(CenterColor)

            # Try to assign colors to this edge (uu, vv)
            for ColorNew in Colors:

                # Assign the color to the current edge, update CommEdgeColorInfo
                # Go to the edge at next depth. If not, return False, show that this color assignment failed, try another color.
                NewColorInfo = assignColorForEdge(uu, vv, NewColorInfo, ComUU, ComVV, ColorNew)
                flag, SearchEdge = PropagandaChecking_recursive(uu, vv, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth-1, SearchEdge)

                # If there is a way to assign the color to a neighbor edge (uu, vv), break the color assignment loop.
                # And check the next neighbor edge
                if flag:
                    break

            # If flag == false, that means no color can be assigned to the current edge.
            # This means no possible color can be set to current neighbor edge.
            # Set the color of this edge back to "black"
            # return false and try another color for the last-level edge.
            if not flag:
                return False, SearchEdge

    return True, SearchEdge


# iterative version
# Check next (depth) level neighbor edges from the given one


# Assign the color to the current edge, update CommEdgeColorInfo, go to the next edge
def assignColorForEdge(u, v, CommEdgeColorInfo, ComU, ComV, Color):
    CommEdgeColorInfo[ComU][u][v]["Color"] = Color
    CommEdgeColorInfo[ComV][v][u]["Color"] = Color
    return CommEdgeColorInfo


# Find appropriate color for the given edge
def findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag):

    if timestep < 0:
        # print("time runs out!")
        return CommEdgeColorInfo, False, timestep

    # edges between two cells
    if not CellToCellEdges:
        return CommEdgeColorInfo, True, timestep

    # Find the tail element of the current CellToCellEdges list. It is an edge. Find this edge's terminal nodes, terminal cell
    u, v = CellToCellEdges[-1]
    ComU, ComV = MergeResult[u], MergeResult[v]
    ColorFlag = False
    NewColorInfo = copy.deepcopy(CommEdgeColorInfo)

    # If this edge (u,v) was colored, skip to the next edge
    if CommEdgeColorInfo[MergeResult[u]][u][v]["Color"] != "black":
        CellToCellEdges.pop()
        NewColorInfo, ColorFlag, timestep = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, NewColorInfo,
                                                           CellToCellEdges, timestep - 1, bio_flag)
        if not ColorFlag:
            CellToCellEdges.append((u, v))

    else:
        # Assign a color
        for Color in ColorOptions:

            # Assign the color to the current edge, then update CommEdgeColorInfo, go to the next edge
            NewColorInfo = assignColorForEdge(u, v, NewColorInfo, ComU, ComV, Color)

            # For bio definition, we can set the same color for the edges outgoing from the same node.
            if bio_flag:
                for vv in NewColorInfo[MergeResult[u]][u]:
                    if vv != v and NewColorInfo[MergeResult[u]][u][vv]['Type'] == "Outgoing":
                        NewColorInfo = assignColorForEdge(u, vv, NewColorInfo, ComU, MergeResult[vv], Color)

            # Check if the current color works for the chosen edge (u, v), the depth of recursion in propaganda checking is set to 5
            depth = 3
            SearchEdge = 500
            flag, SearchEdge = PropagandaChecking_recursive(u, v, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth, SearchEdge)

            if flag:
                print(timestep, SearchEdge, flag, "successful color assignment!")
            else:
                print(timestep, SearchEdge, flag, "failed color assignment!")

            if flag:

                # Temporarily remove the edge from CellToCellEdges, if all edges can be colored correctly, it will be an empty list
                # If the color assignment doesn't follow the constraints, we will add the edge back in the first backtracking step
                CellToCellEdges.pop()
                NewColorInfo, ColorFlag, timestep = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions, NewColorInfo,
                                                         CellToCellEdges, timestep - 1, bio_flag)

                # If the current color assignment can give us the solution for the whole graph, return back
                # If the current color cannot be assigned, go backtracking (first backtracking) and try another color until all the colors used
                if ColorFlag:
                    break
                else:
                    CellToCellEdges.append((u, v))

    # If no color can be assigned to this edge, go backtracking (second backtracking)
    if not ColorFlag:

        # CommEdgeColorInfo was not changed in the color assignment, so we can directly return the original CommEdgeColorInfo
        return CommEdgeColorInfo, False, timestep

    # If ColorFlag == True, that means we find the color assignment solution, return to the last level
    else:
        return NewColorInfo, True, timestep


# Create a dictionary, key is the community number, value is a dictionary.
# The inner dictionary, key is an edge connecting to the community in the last level, value is its color
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
                    D[ComU][u] = {v: {"Type": "Outgoing", "Color": "black"}}

                if v in D[ComV]:
                    D[ComV][v][u] = {"Type": "Incoming", "Color": "black"}
                else:
                    D[ComV][v] = {u: {"Type": "Incoming", "Color": "black"}}

    return D, CellToCellEdges


def ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions):

    # Create a dictionary, key is the community number, value is a dictionary.
    # The inner dictionary, key is an edge connecting to the community in the last level, value is its color
    CommEdgeColorInfo, CellToCellEdges = createColorInfo(MergeResult, CommunityNumToNodes, G_primitive)

    # Color the cell-cell edges
    timestep = 10000
    CommEdgeColorInfo, ColorFlag, _ = findColor(MergeResult, CommunityNumToNodes, DAG, ColorOptions[2:], CommEdgeColorInfo, CellToCellEdges, timestep,
                                             bio_flag)

    for u, v in DAG.edges:
        Color = "black"

        # If the edge doesn't exist in G_primitive, set it as "black"
        # black edges are input or output edges for the whole graph
        if u in MergeResult and v in MergeResult:

            # If the edge is inside a community, set it "gray"
            if MergeResult[u] == MergeResult[v]:
                Color = "gray"

            # Otherwise, it is cell-cell edge. change the color for the edge
            else:
                Color = CommEdgeColorInfo[MergeResult[u]][u][v]["Color"]
        DAG.add_edge(u, v, color=Color)

    return ColorFlag, DAG


def startColoring(ColorOptions):
    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Verify samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, _, bio_flag, _, _, _, _, _ = utils.loadData(s, settings)
        target_n = math.ceil(len(G_primitive.nodes) / S_bounds[1])
        MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge.txt", s)
        DAG = utils.load_graph(settings, s)
        CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)

        ColorFlag, DAG = ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions)

        if ColorFlag:
            # Write edge list with color
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)
        else:
            print("Cannot find appropriate solution for edge coloring!")
            iof.writeColoredEdgeList(out_path, '/sol_after_merge_colored.txt', DAG)


# Assume we have totally 4 different cell-cell communication molecular, set 4 as the input parameter. Then we will give the solution with numbers.
ColorOptions = ["black", "gray", "color1", "color2", "color3", "color4", "color5", "color6", "color7", "color8", "color9", "color10"]
startColoring(ColorOptions)


