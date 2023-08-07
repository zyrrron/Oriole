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

        # if this neighbor edge has no color, nothing will be broken
        if ColorInfo[ComUU][uu][vv]["Color"] != "black":

            # Only accept same color between neighbor edge and center edge when it is under bio definition and have same source point
            if ColorInfo[ComUU][uu][vv]["Color"] == CenterColor:
                if not (bio_flag and uu == u):
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

    # find current center edge's color and check its neighbors, see if this edge's color can meet all constraints.
    CenterColor = ColorInfo[MergeResult[u]][u][v]["Color"]
    NeighborEdges = ef.findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, ColorInfo, bio_flag)
    NewColorInfo = copy.deepcopy(ColorInfo)

    # Create color options for each neighbor edge.
    # Regularly, edges cannot be assigned with the same color as the center edge.
    # Remove center color from current edge's color options if it does not have same source point with center edge.
    # Bio definition allows the edges has the same source with center edge (u, v) be assigned with the same color.
    # Try the center color at first, then others.
    LeftColor = {}
    for edge in NeighborEdges:
        LeftColor[edge] = copy.deepcopy(ColorOptions)
        LeftColor[edge].remove(CenterColor)
        if bio_flag and edge[0] == u:
            LeftColor[edge].insert(0, CenterColor)

    # Check if the center edge is colored without breaking any constraint.
    # if not, return false
    if not checkNeighborColor(u, v, CenterColor, NeighborEdges, NewColorInfo, MergeResult, bio_flag):
        return False, SearchEdge

    # max depth is arrived, return back
    # max number of edges we want to check in this
    if depth <= 0 or SearchEdge < 0:
        return True, SearchEdge

    # index is the pointer for the edge to be checked in the next iteration. Go through back from end to begin
    # Keep trying to assign colors to the neighbor edges of (u, v) until NeighborEdges are all successfully colored or the first edge to be checked
    # has no more colors left to be assigned.
    index = len(NeighborEdges) - 1
    while 0 <= index < len(NeighborEdges):
        (uu, vv) = NeighborEdges[index]

        # If the edges we have searched is more than the value of given original SearchEdge, it means the edge coloring still has possibility to find
        # correct coloring assignment in the future, we can accept this non-deterministic and return True
        if SearchEdge < 0:
            return True, 0
        SearchEdge -= 1

        # If there is an edge cannot be assigned to any color, flag = false
        flag = False
        ComUU, ComVV = MergeResult[uu], MergeResult[vv]

        # For the edges has colors, we have checked it in the first "if" statement: checkNeighborColor().
        # But after that, we still assigned some new colors to the edges around (uu,vv). It still need to be checked.
        if ColorInfo[ComUU][uu][vv]["Color"] != "black":
            NeighborEdgesNew = ef.findNeighborEdges(uu, vv, MergeResult, CommunityNumToNodes, ColorInfo, bio_flag)

            # If meet all constraints, go to the next iteration, index--
            # If not, try other colors for this edge.
            if checkNeighborColor(uu, vv, ColorInfo[ComUU][uu][vv]["Color"], NeighborEdgesNew, NewColorInfo, MergeResult, bio_flag):
                index -= 1
                continue

        # Try to assign colors to this edge (uu, vv) from the left colors
        while LeftColor[(uu, vv)]:

            # Assign the color to the current edge, update NewColorInfo
            # Update LeftColor[(uu, vv)]
            # Go to the edge at next depth. If flag = false, return False, show that this color assignment failed, try another color.
            Color = LeftColor[(uu, vv)].pop(0)
            NewColorInfo = assignColorForEdge(uu, vv, NewColorInfo, ComUU, ComVV, Color)
            flag, SearchEdge = PropagandaChecking_recursive(uu, vv, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth-1, SearchEdge)

            # If there is a way to assign the color to a neighbor edge (uu, vv), update index, break the color assignment loop for (uu, vv).
            # And check the next neighbor edge
            if flag:
                index -= 1
                break

        # If flag == false, that means no color can be assigned to the current edge.
        # This means no possible color can be set to current neighbor edge.
        # Set the left color of this edge back to original color options
        # This failure for edge (uu, vv) might be caused by the other neighbor edges from "NeighborEdges", so we can go back to the last neighbor edge
        # Update index and try the last neighbor edge.
        if not flag:
            index += 1
            edge = (uu, vv)
            LeftColor[edge] = copy.deepcopy(ColorOptions)
            LeftColor[edge].remove(CenterColor)
            if bio_flag and edge[0] == u:
                LeftColor[edge].insert(0, CenterColor)

    return True, SearchEdge


# Assign the color to the current edge, update CommEdgeColorInfo, go to the next edge
def assignColorForEdge(u, v, CommEdgeColorInfo, ComU, ComV, Color):
    CommEdgeColorInfo[ComU][u][v]["Color"] = Color
    CommEdgeColorInfo[ComV][v][u]["Color"] = Color
    return CommEdgeColorInfo


# Find appropriate color for the given edge, recursive
def findColor_r(MergeResult, CommunityNumToNodes, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag):

    if timestep < 0:
        # print("time runs out!")
        return CommEdgeColorInfo, False, timestep

    # if this list is empty, that means no more edges can be colored later.
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
        NewColorInfo, ColorFlag, timestep = findColor_r(MergeResult, CommunityNumToNodes, ColorOptions, NewColorInfo,
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
            print(timestep, SearchEdge, flag, (u, v))


            if flag:

                # Temporarily remove the edge from CellToCellEdges, if all edges can be colored correctly, it will be an empty list
                # If the color assignment doesn't follow the constraints, we will add the edge back in the first backtracking step
                CellToCellEdges.pop()
                NewColorInfo, ColorFlag, timestep = findColor_r(MergeResult, CommunityNumToNodes, ColorOptions, NewColorInfo,
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


# Find appropriate color for the given edge, iterative
def findColor(MergeResult, CommunityNumToNodes, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag):

    CellToCellEdges = [('c', 'd'), ('b', 'c'), ('b', 'a'), ('c', 'a'), ('e', 'c'), ('a', 'e'), ('e', 'd')]

    # Create dictionary LeftColor, key is an edge, value shows all the colors have not been tried for this edge yet.
    # Loop through the elements in the list CellToCellEdges
    # Assign the ColorOptions list as the value for each key in the dictionary
    LeftColor = {}
    for edge in CellToCellEdges:
        LeftColor[edge] = copy.deepcopy(ColorOptions)

    # If Forward = False, that means it comes back from edges failed to be colored. So we need try other colors for this
    Forward = True
    EdgeTotalNum = len(CellToCellEdges)
    stack = [(CellToCellEdges, CommEdgeColorInfo, timestep, Forward)]

    while stack:
        CellToCellEdges, CommEdgeColorInfo, timestep, Forward = stack.pop()

        # If the first edge cannot be colored successfully by the first color, same with other colors. So we can return False directly.
        if len(CellToCellEdges) == EdgeTotalNum and not Forward:
            return CommEdgeColorInfo, False, timestep

        # Check if the time limit has been reached, return the current status
        if timestep < 0:
            return CommEdgeColorInfo, False, timestep

        # If there are no more edges to color, the process is complete, return the current status
        if not CellToCellEdges:
            return CommEdgeColorInfo, True, timestep

        # Get the last edge in the list of cell-cell edges, and the colors left to be assigned.
        # ColorFlag shows if there is one color that can be accepted
        u, v = CellToCellEdges[-1]
        ComU, ComV = MergeResult[u], MergeResult[v]
        ColorFlag = False
        NewColorInfo = copy.deepcopy(CommEdgeColorInfo)

        # If the current edge (u, v) was already colored
        if NewColorInfo[ComU][u][v]["Color"] != "black":

            # If the current edge's color meet all the constraints now and it is not come backward (backward means it fails to color the later edges).
            # Then continue to the next edge
            NeighborEdges = ef.findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, NewColorInfo, bio_flag)
            if checkNeighborColor(u, v, NewColorInfo[ComU][u][v]["Color"], NeighborEdges, NewColorInfo, MergeResult, bio_flag) and Forward:

                # Push current important variables to stack. Then remove the edge we checked in this iteration and go to the next iteration.
                # Add 1 to the number of searched edges.
                stack.append((CellToCellEdges, NewColorInfo, timestep - 1, True))
                CellToCellEdges.pop()
                print(timestep, -1, True, (u, v), NewColorInfo[ComU][u][v], "color has been assigned successfully before this step!")
                continue

            # If that edge's color cannot meet all the constraints now, try other colors in the later part
            else:
                NewColorInfo[ComU][u][v]["Color"] = "black"

        # No matter if the current edge (u,v) was colored, we need to update the to be checked color list according to the tried colors.
        Colors = LeftColor[(u, v)]

        # Try different colors for the current edge (u, v)
        for Color in Colors:

            # Try a new color, assign it to edge (u, v), remove this color from the Leftcolor list for edge (u, v)
            LeftColor[(u, v)].remove(Color)
            NewColorInfo = assignColorForEdge(u, v, NewColorInfo, ComU, ComV, Color)

            # The depth of recursion in the propaganda checking step
            depth = 3
            # The number of edges to search during the propaganda checking step
            SearchEdge_upperbound = 500
            # Propaganda checking with constraints for depth and number of edge to be searched
            flag, SearchEdge_checked = PropagandaChecking_recursive(u, v, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth, SearchEdge_upperbound)

            # output "SearchEdge_check = -1" means color has been assigned before this step
            # output "SearchEdge_check = 0" means searched upperbound number of edges
            # output "SearchEdge_check = 500" means color has been assigned before this step
            if flag:
                print(timestep, f"{SearchEdge_upperbound - SearchEdge_checked} edge(s) are checked", flag, (u, v), NewColorInfo[MergeResult[u]][u][v])
            else:
                print(timestep, f"{SearchEdge_upperbound - SearchEdge_checked} edge(s) are checked", flag, (u, v), f"{Color} failed!")

            # If a valid color is found for the current edge, continue with the next edge
            if flag:
                CellToCellEdges.pop()
                stack.append((CellToCellEdges, NewColorInfo, timestep - 1, True))
                ColorFlag = True
                break

        # If no valid color is found for the current edge, backtrack to the previous edge and try another color for the previous edge
        if not ColorFlag:
            CellToCellEdges.append((u, v))
            stack.append((CellToCellEdges, CommEdgeColorInfo, timestep - 1, False))

    # If no color can be assigned to any edge, return False
    return CommEdgeColorInfo, False, timestep


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
    CommEdgeColorInfo, ColorFlag, timestep_used = findColor(MergeResult, CommunityNumToNodes, ColorOptions[2:], CommEdgeColorInfo, CellToCellEdges, timestep,
                                             bio_flag)

    if ColorFlag:
        print(f"Find solution with {timestep- timestep_used} timestep(s)")
    else:
        if timestep > 0:
            print("Try all possible coloring assignment but no solution is found!")
        else:
            print("Time runs out! Set timestep bigger next time!")
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
# , "color4", "color5", "color6", "color7", "color8", "color9", "color10"
ColorOptions = ["black", "gray", "color1", "color2", "color3"]
startColoring(ColorOptions)


