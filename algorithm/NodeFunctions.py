import networkx as nx

# Find all neighbor nodes round the given node in G.
def findAllNeighbors(node, G):
    return nx.all_neighbors(G, node)


# Find all neighbor nodes round the given community in G.
def findAllNeighborsComm(node, G):
    return nx.all_neighbors(G, node)
