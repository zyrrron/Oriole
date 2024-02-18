# Set the number of cell-cell communication as the input parameters
# Assign coloring remarks for each edge in a dictionary and save it.
import copy
import InOutFunctions as iof
import UpdateFunctions as uf
import json
import csv
import utils
import EdgeFunctions as ef
import collections
import time


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


# If the color options (domain) reduce to only one, try assign the colors of neighbor edges for (u,v), can go to deeper depth.
# Check the Neighbor Edges one by one.
# Constraint 1: neighbor edges can share the same color if they are from the same node.
# Constraint 2: neighbor edges cannot share the same color unless they are from the same node.
# Constraint 3: edges can share the same color if they are not neighbor edges.
# Step 1: If the edge is colored and use the same with the given checking edge, then return False
# Step 2: If the edge is not colored, choose one color from currently optional color domain.
# Recursive version
def PropagandaChecking(u, v, MergeResult, CommunityNumToNodes, ColorInfo, ColorOptions, bio_flag, depth, SearchEdge):

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
        return True, 0

    # index is the pointer for the edge to be checked in the next iteration. Go through back from end to begin
    # Keep trying to assign colors to the neighbor edges of (u, v) until NeighborEdges are all successfully colored or the first edge to be checked
    # has no more colors left to be assigned.
    index = len(NeighborEdges) - 1
    while 0 <= index < len(NeighborEdges):
        (uu, vv) = NeighborEdges[index]

        # If the edges we have searched is more than the value of given original SearchEdge, it means the edge coloring still has possibility to find
        # correct coloring assignment in the future, we can accept this non-deterministic and return True
        if SearchEdge <= 0:
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
            flag, SearchEdge = PropagandaChecking(uu, vv, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth-1, SearchEdge)

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


# Find appropriate color for the given edge, iterative
def findColor(MergeResult, CommunityNumToNodes, ColorOptions, CommEdgeColorInfo, CellToCellEdges, timestep, bio_flag):

    # CellToCellEdges = [('c', 'd'), ('b', 'c'), ('b', 'a'), ('c', 'a'), ('e', 'c'), ('a', 'e'), ('e', 'd')]

    # Create dictionary LeftColor, key is an edge, value shows all the colors have not been tried for this edge yet.
    # Loop through the elements in the list CellToCellEdges
    # Assign the pointer in the ColorOptions list as the value for each key in the dictionary NextColorIndex
    NextColorIndex = {}
    for edge in CellToCellEdges:
        NextColorIndex[edge] = 0

    # If Forward = False, that means it comes back from edges failed to be colored. So we need try other colors for this
    Forward = True
    EdgeTotalNum = len(CellToCellEdges)
    index = EdgeTotalNum - 1
    NewColorInfo = copy.deepcopy(CommEdgeColorInfo)

    # index == 0 means there is no more edges to color, the process is complete, return the current status
    while 0 <= index:

        # if timestep % 1000 == 0:


        # If the first edge cannot be colored successfully by the first color, same with other colors. So we can return False directly.
        if index >= EdgeTotalNum-1 and not Forward:
            print("Edge index:", index, ", Time step:", timestep, ", Edges colored: ", EdgeTotalNum-index-1, ", Color percentage:", 1-((index+1) / EdgeTotalNum))
            return NewColorInfo, False, timestep, index

        # Check if the time limit has been reached, return the current status
        if index > timestep:
            print("Edge index:", index, ", Time step left:", timestep, ", Edges colored: ", EdgeTotalNum-index-1, ", Color percentage:", 1-((index+1) / EdgeTotalNum))
            return NewColorInfo, False, timestep, index

        # Get the index-th edge in the list of cell-cell edges, and the colors left to be assigned.
        # ColorFlag shows if there is one color that can be accepted
        u, v = CellToCellEdges[index]
        ComU, ComV = MergeResult[u], MergeResult[v]
        ColorFlag = False

        # If the current edge (u, v) was already colored
        if NewColorInfo[ComU][u][v]["Color"] != "black":

            # If the current edge's color meet all the constraints now and it is not come backward
            # (backward means it fails to color the (index-1)-th edge).
            # Then continue to the next edge
            # If that edge's color cannot meet all the constraints now, try other colors in the later part. No need for extra action here.
            NeighborEdges = ef.findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, NewColorInfo, bio_flag)
            if checkNeighborColor(u, v, NewColorInfo[ComU][u][v]["Color"], NeighborEdges, NewColorInfo, MergeResult, bio_flag) and Forward:

                # Update index and go to the next iteration
                # print(timestep, -1, True, index, (u, v), NewColorInfo[ComU][u][v], "color has been assigned successfully before this step!")
                index -= 1
                timestep -= 1
                continue

        # No matter if the current edge (u,v) was colored, we need to update the to be checked color list according to the tried colors.
        # Try different colors for the current edge (u, v) until color list is empty
        Colors = ColorOptions[NextColorIndex[(u, v)]:]
        for Color in Colors:

            # Try a new color, assign it to edge (u, v), remove this color from the LeftColor list for edge (u, v)
            NextColorIndex[(u, v)] += 1
            NewColorInfo = assignColorForEdge(u, v, NewColorInfo, ComU, ComV, Color)

            # Set same color to the same-source edge (u, vv)
            # If this edge has color, don't change it. Because this color has been accepted in the previous iterations.
            # Because the current color index is the first color that allow its one previously-checked neighbor meet all constraints
            # The previous colors before the current color index were all failed.
            for vv in NewColorInfo[ComU][u]:
                if NewColorInfo[ComU][u][vv]["Color"] == "black" and NewColorInfo[ComU][u][vv]["Type"] == "Outgoing" and vv != v:
                    NextColorIndex[(u, vv)] = NextColorIndex[(u, v)]
                    ComVV = MergeResult[vv]
                    NewColorInfo = assignColorForEdge(u, vv, NewColorInfo, ComU, ComVV, Color)
                    # print("Neighbor edges: ", (u, vv), ColorOptions[NextColorIndex[(u, vv)]:])

            # The depth of recursion in the propagation checking step
            # The number of edges to search during the propagation checking step
            # Propagation checking with constraints for depth and number of edge to be searched
            depth = 3
            SearchEdge = 50

            # If the color options (domain) reduce to only one, try assign the colors of neighbor edges for (u,v), can go to deeper depth.
            # Even depth and SearchEdge is both 0, PropagandaChecking() will also check current edge meet all constraints for neighbor edges.
            if len(ColorOptions) <= NextColorIndex[(u, v)]+1:
                depth, SearchEdge = 0, 0
            flag, SearchEdge_left = PropagandaChecking(u, v, MergeResult, CommunityNumToNodes, NewColorInfo, ColorOptions, bio_flag, depth, SearchEdge)

            # output "SearchEdge_check = -1" means color has been assigned before this step
            # output "SearchEdge_check = 0" means searched upperbound number of edges
            # output "SearchEdge_check = 500" means color has been assigned before this step
            # if flag:
            #     print(timestep, f"{SearchEdge - SearchEdge_left} edge(s) are checked", flag, index, (u, v), NewColorInfo[MergeResult[u]][u][v])
            # else:
            #     print(timestep, f"{SearchEdge - SearchEdge_left} edge(s) are checked", flag, index, (u, v), f"{Color} failed!")

            # No matter if the color in this iteration is correct for the edge (uu, vv), timestep--
            # If it is correct, break the loop and update edge index, ColorFlag, Forward
            # If not, keep searching the colors until the colors list is empty
            timestep -= 1
            if flag:
                index -= 1
                Forward = True
                ColorFlag = True
                break

        # If no valid color is found for the current edge, backtrack to the previous edge and try another color for the previous edge
        if not ColorFlag:
            index += 1
            Forward = False
            NextColorIndex[(u, v)] = 0

        # print out the left colors for the current edge (u,v)
        # print(index, (u,v), ColorOptions[NextColorIndex[(u, v)]:])

    # If no color can be assigned to any edge, return False
    return NewColorInfo, True, timestep, index


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


def ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions, timestep_reback):

    # Create a dictionary, key is the community number, value is a dictionary.
    # The inner dictionary, key is an edge connecting to the community in the last level, value is its color
    CommEdgeColorInfo, CellToCellEdges = createColorInfo(MergeResult, CommunityNumToNodes, G_primitive)
    timestep = timestep_reback + len(CellToCellEdges)

    # Color the cell-cell edges
    CommEdgeColorInfo, ColorFlag, timestep_used, EdgeIndex = findColor(MergeResult, CommunityNumToNodes, ColorOptions[2:], CommEdgeColorInfo,
                                                                       CellToCellEdges, timestep, bio_flag)

    # if ColorFlag:
    #     print(f"Find solution for coloring {len(CellToCellEdges)} cell to cell edges with {timestep- timestep_used} timestep(s)")
    # else:
    #     if timestep > 0:
    #         print("Color assignment failed, try another partition result!")
    #     else:
    #         print("Time runs out! Set timestep bigger next time!")
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
    return ColorFlag, DAG, EdgeIndex, len(CellToCellEdges)


def startColoring(upperbounds, SingleFlag=True):

    # Load samples and settings
    samples, settings = utils.loadSettings()

    # Assign colors to each cell-cell edge iteratively
    for ele in range(len(samples)):
        s = samples[ele]
        upperbound = upperbounds[ele]
        print(f"try to assign with {upperbound} colors")
        ColorOptions = ["black", "gray"]
        for j in range(upperbound):
            ColorOptions.append(f"color{j}")

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, _, _, bio_flag, _, _, _, attempt_range, _ = utils.loadData(s, settings)
        ColorFlag = True
        DAG = utils.load_graph(settings, s)
        begin_time = time.time()
        timestep_reback = 20000

        if SingleFlag:
            # Only check one solution file
            MergeResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}.txt", s)
            CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
            ColorFlag, DAG, EdgeIndex, TotalEdges = ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions, timestep_reback)

        else:
            # Check a list of potential solution with minimum length
            json_file = open(f"{out_path}/merge_result_list_{S_bounds[1]}_{constraint[0]}_{attempt_range}.json", "r")
            json_data = json_file.read()
            json_file.close()
            MergeResultList = json.loads(json_data)
            PreviousSolLength = 0

            # check result list with different attempt range
            # Allow 500000 trace back steps.
            checklist = []
            if attempt_range == [1, 5]:
                checklist = [7196]
            elif attempt_range == [5, 10]:
                checklist = [12490]
            elif attempt_range == [1, 10]:
                timestep_reback = 5000
                for i in range(len(MergeResultList)):
                    if 92 <= MergeResultList[i][0] <= 93:
                        checklist.append(i)
            else:
                checklist = range(8000, len(MergeResultList), 200)

            # timestepOld = 10000
            # with open(f"{out_path}/EdgeIndexInfo_{timestepOld}.csv", "r") as csv_file:
            #     reader = csv.reader(csv_file)
            #     next(reader)
            #     data = list(reader)
            # top_names = [int(row[0]) for row in data[:50]]

            # create a csv file saving the deepest edge for one solution has searched.

            EdgeIndexInfo_file = open(f"{out_path}/EdgeIndexInfo_{attempt_range}_{timestep_reback}_{len(ColorOptions)-2}.csv", "a", newline="")
            writer = csv.writer(EdgeIndexInfo_file)
            if EdgeIndexInfo_file.tell() == 0:
                writer.writerow(["Solution index", "Edge index", "Total cell-cell edges", "Edges colored", "Color percentage"])

            # Check merge solution respectively
            for i in checklist:
                SolLength, MergeResult = MergeResultList[i]
                if SolLength != PreviousSolLength:
                    PreviousSolLength = SolLength
                    print(f"Now check the result with {SolLength} communities")

                # print index of current solution
                print(i)
                CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
                ColorFlag, DAG, EdgeIndex, TotalEdges = ColorAssignment(MergeResult, CommunityNumToNodes, G_primitive, DAG, bio_flag, ColorOptions, timestep_reback)
                writer.writerow([i, EdgeIndex, TotalEdges, TotalEdges - EdgeIndex - 1, (TotalEdges - EdgeIndex - 1) / TotalEdges])
                if ColorFlag:
                    CostTime = time.time() - begin_time
                    iof.writeSolution(out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{len(ColorOptions)-2}.txt', G_primitive, MergeResult, CostTime)
                    break

        CostTime = time.time() - begin_time
        if ColorFlag:
            # Write edge list with color
            print(f"Find appropriate solution for edge coloring! Run time: {CostTime}")
            iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{len(ColorOptions)-2}_colored.txt', DAG)
        else:
            print(f"Cannot find appropriate solution for edge coloring! Run time: {CostTime}")
            iof.writeColoredEdgeList(out_path, f'/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{len(ColorOptions)-2}_colored.txt', DAG)


# Assume we have totally 4 different cell-cell communication molecular, set 4 as the color parameter.
# Set color list
# SingleFlag = True: Only check one solution file
# SingleFlag = False: Check a list of potential solution
# upperbounds = [7, 6]
# startColoring(upperbounds, False)


