import EdgeFunctions as ef

# check indegree/outdegree constraints for a given community
def checkInOut(G, community, constraint):
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


# check loop in current community
def checkLoop():
    pass


# check and find the worst case in PendingCommunities
def findWorstCommunity(PendingCommunities):
    maxVal = 0
    maxKey = ''
    for key in PendingCommunities:
        if PendingCommunities[key] > maxVal:
            maxKey = key
    return maxKey