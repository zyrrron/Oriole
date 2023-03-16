import EdgeFunctions as ef
import networkx as nx
import UpdateFunctions as uf

# check indegree/outdegree constraints for a given community
def checkInOut(G, community, constraint, CurrentVerifyResult):
    InEdges = ef.findIncomingEdges(G, community)
    OutEdges = ef.findOutgoingEdges(G, community)
    # check high constraint
    if len(constraint) == 2:
        if len(InEdges) <= constraint[0] and len(OutEdges) <= constraint[1]:
            return 0
        else:
            return max(0, len(InEdges)-constraint[0]) + max(0, len(OutEdges)-constraint[1])
    # check low constraint
    else:
        if len(InEdges) + len(OutEdges) <= constraint[0]:
            return 0
        else:
            return len(InEdges) + len(OutEdges) - constraint


# check community size
def checkSize():
    pass


# Find all neighbor nodes around the given community in G.
def findAllNeighborsComm(node, G):
    return nx.all_neighbors(G, node)


# Find all incoming edges to Community C, need to do
def findIncomingEdgesComm(G, c, CurrentVerifyResult):
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentVerifyResult)
    InEdges = []
    # Collect all incoming edges and outgoing edges for the nodes in community c
    for node in c:
        tmp = ef.findIncomingEdges(G, node)
        for t in tmp:
            InEdges.append(t)

    # select the Incoming edges for the community c
    InEdgesComm = []
    for ele in list(InEdges):
        # ele[1] must be in c, because it is an incoming edge, end node must in c.
        if ele[0] not in CommunityNumToNodes[c]:
            InEdgesComm.append(ele)
        else: print(ele)

    return InEdgesComm


# Find all outgoing edges from Community C, need to do
def findOutgoingEdgesComm(G, c, CurrentVerifyResult):
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentVerifyResult)
    OutEdges = []

    # Collect all incoming edges and outgoing edges for the nodes in community c
    for node in c:
        tmp = ef.findOutgoingEdges(G, node)
        for t in tmp:
            OutEdges.append(t)

    # select the Outgoing edges for the community c
    OutEdgesComm = []
    for ele in list(OutEdges):
        # ele[1] must be in c, because it is an incoming edge, end node must in c.
        if ele[0] not in CommunityNumToNodes[c]:
            OutEdgesComm.append(ele)
        else:
            print(ele)
    return OutEdgesComm


# Add neighbor Community into current pending community
def addNeighborComm(CurrentVerifyResult, NeighborComm, PendingCommunity):
    return CurrentVerifyResult


# check loop in current community
def checkLoop(G, community, CurrentVerifyResult):
    return 0


# check and find the worst case in PendingCommunities
def findWorstCommunity(G, PendingCommunities, CurrentVerifyResult):
    maxVal = 0
    maxKey = ''
    maxEdges = 0
    for key in PendingCommunities:
        # update the worst case when a community has bigger value
        if PendingCommunities[key] > maxVal:
            maxKey = key
            maxEdges = findIncomingEdgesComm(G, key, CurrentVerifyResult) + findOutgoingEdgesComm(G, key, CurrentVerifyResult)

        # If the number of unmet constraints is equal, choose the one has more edges connected
        if PendingCommunities[key] == maxVal:
            if findIncomingEdgesComm(G, key, CurrentVerifyResult) + findOutgoingEdgesComm(G, key, CurrentVerifyResult) > maxEdges:
                maxKey = key
                maxEdges = findIncomingEdgesComm(G, key, CurrentVerifyResult) + findOutgoingEdgesComm(G, key, CurrentVerifyResult)
    return maxKey


# Find the communities that cannot meet all constraints, if there is no pending community exists, return -1, else return its community number
def findPendingCommunities(G, result, constraint):
    PendingCommunities = {}
    for key in result:
        res = checkInOut(G, key, constraint, result) + checkLoop(G, key, result)
        if res != 0:
            PendingCommunities[key] = res
    print(PendingCommunities)
    return PendingCommunities