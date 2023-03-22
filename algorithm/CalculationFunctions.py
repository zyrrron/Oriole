import EdgeFunctions as ef
import CommunityFunctions as ccf

def calculateDegreeAndCycle(G, C, R):
    Indegree = len(ccf.findIncomingEdgesComm(G, C, R))
    Outdegree = len(ccf.findOutgoingEdgesComm(G, C, R))
    Cycle = ccf.checkLoopComm(G, C, R)
    return Indegree, Outdegree, Cycle

# calculate the rewards that one node can provide after adding it to the community
def calculateRewardComm(G, NeighborComm, PendingCommunity, CurrentResult, constraint):

    # Save original data
    OriginalIndegree, OriginalOutdegree, OriginalCycle = calculateDegreeAndCycle(G, PendingCommunity, CurrentResult)

    # Update current verify result after adding this neighbor community
    CurrentResult_new = ccf.addNeighborComm(CurrentResult, NeighborComm, PendingCommunity)

    # Calculate the new data
    NewIndegree, NewOutdegree, NewCycle = calculateDegreeAndCycle(G, PendingCommunity, CurrentResult_new)

    # r1: indegree gain; r2: outdegree gain; r3: cycle gain
    r1, r2, r3 = 0, 0, OriginalCycle - NewCycle

    # high constraint
    if len(constraint) == 2:
        r1 = max(OriginalIndegree, constraint[0]) - NewIndegree
        r2 = max(OriginalOutdegree, constraint[1]) - NewOutdegree

    # low constraint
    else:
        r1 = max(OriginalIndegree + OriginalOutdegree, constraint) - NewIndegree - NewOutdegree

    return r1 + r2 + r3
