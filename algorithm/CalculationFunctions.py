import EdgeFunctions as ef
import CommunityFunctions as ccf

# calculate the rewards that one node can provide after adding it to the community
def calculateReward(G, NeighborComm, PendingCommunity, CurrentVerifyResult, constraint):
    # r1: indegree gain; r2: outdegree gain; r3: cycle gain
    OriginalIndegree = ef.findIncomingEdgesComm(G, PendingCommunity, CurrentVerifyResult)
    OriginalOutdegree = ef.findOutgoingEdgesComm(G, PendingCommunity, CurrentVerifyResult)
    OriginalCycle = ccf.findCyleComm(G, PendingCommunity, CurrentVerifyResult)

    # update current verify result after adding this neighbor community
    CurrentVerifyResult_new = ccf.addNeighborComm(CurrentVerifyResult, NeighborComm, PendingCommunity)

    NewIndegree = ef.findIncomingEdgesComm(G, PendingCommunity, CurrentVerifyResult)
    NewOutdegree = ef.findOutgoingEdgesComm(G, PendingCommunity, CurrentVerifyResult)
    NewCycle = ccf.findCyleComm(G, PendingCommunity, CurrentVerifyResult)

    r1, r2, r3 = 0, 0, OriginalCycle - NewCycle
    # high constraint
    if len(constraint) == 2:
        r1 = max(OriginalIndegree, constraint[0]) - NewIndegree
        r2 = max(OriginalOutdegree, constraint[1]) - NewOutdegree
    else:
        r1 = max(OriginalIndegree + OriginalOutdegree, constraint) - NewIndegree - NewOutdegree

    return r1 + r2 + r3