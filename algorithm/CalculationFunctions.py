import EdgeFunctions as ef
import CommunityFunctions as ccf

# calculate the rewards that one node can provide after adding it to the community
def calculateRewardComm(G, NeighborComm, PendingCommunity, CurrentResult, constraint):
    # r1: indegree gain; r2: outdegree gain; r3: cycle gain
    OriginalIndegree = len(ccf.findIncomingEdgesComm(G, PendingCommunity, CurrentResult))
    OriginalOutdegree = len(ccf.findOutgoingEdgesComm(G, PendingCommunity, CurrentResult))
    OriginalCycle = ccf.checkLoopComm(G, PendingCommunity, CurrentResult)

    # update current verify result after adding this neighbor community
    CurrentResult_new = ccf.addNeighborComm(CurrentResult, NeighborComm, PendingCommunity)

    NewIndegree = len(ccf.findIncomingEdgesComm(G, PendingCommunity, CurrentResult_new))
    NewOutdegree = len(ccf.findOutgoingEdgesComm(G, PendingCommunity, CurrentResult_new))
    NewCycle = ccf.checkLoopComm(G, PendingCommunity, CurrentResult_new)

    r1, r2, r3 = 0, 0, OriginalCycle - NewCycle
    # high constraint
    if len(constraint) == 2:
        r1 = max(OriginalIndegree, constraint[0]) - NewIndegree
        r2 = max(OriginalOutdegree, constraint[1]) - NewOutdegree
    else:
        r1 = max(OriginalIndegree + OriginalOutdegree, constraint) - NewIndegree - NewOutdegree

    return r1 + r2 + r3