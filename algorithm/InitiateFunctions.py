import networkx as nx

# Put each node in a graph into a distinct community
# Each node says: I am my own community
def createInitialCommunities(G):
    d = {}
    for ele in G.nodes:
        d[ele] = ele
    return d


# Create the subnetwork centering with the pending community
def createSubNetwork(G, PendingCommunities):
    nodes = getNodesFromCommunity(PendingCommunities)
    return


# Get all nodes in the given community
def getNodesFromCommunity(PendingCommunities):
    pass