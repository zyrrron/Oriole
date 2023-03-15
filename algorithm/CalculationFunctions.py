import EdgeFunctions as ef

# calculate the rewards that one node can provide after adding it to the community
def calculateReward(G, node, PendingCommunity, CurrentVerifyResult):
    # r1: indegree gain; r2: outdegree gain; r3: cycle gain
    OriginalIndegree = ef.findIncomingEdgesComm(G, PendingCommunity)
    OriginalOutdegree = ef.findOutgoingEdgesComm(G, PendingCommunity)



    rewards = r1 + r2 + r3