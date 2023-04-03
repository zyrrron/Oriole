import networkx as nx


# Find all incoming edges to node N
def findIncomingEdges(G, n):
    return G.in_edges(n)


# Find all outgoing edges from node N
def findOutgoingEdges(G, n):
    return G.edges(n)


# Find all neighbor edges of an edge.
# Neighbor edge: a cell-cell edge sharing the same terminal cell with the given edeg.
def findNeighborEdges(u, v, MergeResult, CommunityNumToNodes, CommEdgeColorInfo, bio_flag):

    l = []

    return l

