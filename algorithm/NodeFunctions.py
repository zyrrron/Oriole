import networkx as nx

# Find all neighbor nodes around the given node in G.
def findAllNeighbors(node, G):
    return nx.all_neighbors(G, node)


