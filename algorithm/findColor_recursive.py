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
