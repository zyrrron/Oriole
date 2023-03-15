import networkx as nx

# Find all incoming edges to node N
def findIncomingEdges(G, n):
    return G.in_edges(n)


# Find all outgoing edges from node N
def findOutgoingEdges(G, n):
    return G.edges(n)

