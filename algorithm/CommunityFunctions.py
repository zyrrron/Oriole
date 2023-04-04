import EdgeFunctions as ef
import networkx as nx
import UpdateFunctions as uf
import copy


# check indegree/outdegree constraints for a given community
def checkInOutComm(G, community, constraint, CurrentResult, bio_flag):
    InEdges = findIncomingEdgesComm(G, community, CurrentResult, bio_flag)
    OutEdges = findOutgoingEdgesComm(G, community, CurrentResult, bio_flag)

    # Check high constraint
    if len(constraint) == 2:
        if len(InEdges) <= constraint[0] and len(OutEdges) <= constraint[1]:
            return 0
        else:
            return max(0, len(InEdges)-constraint[0]) + max(0, len(OutEdges)-constraint[1])

    # Check low constraint
    else:
        if len(InEdges) + len(OutEdges) <= constraint[0]:
            return 0
        else:
            return len(InEdges) + len(OutEdges) - constraint[0]


# check community size
def checkSize(CurrentResult, PendingCommunity):
    size = 0
    for key in CurrentResult:
        if CurrentResult[key] == PendingCommunity:
            size += 1
    return size


# Find all neighbor communities around the given community c in G.
def findAllNeighborsComm(G, c, CurrentResult):

    # collect all neighbor nodes for the nodes inside community c
    NeighborNodes = set()
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
    for node in CommunityNumToNodes[c]:
        tmp = nx.all_neighbors(G, node)
        for t in tmp:
            NeighborNodes.add(t)

    # find the neighbor communities according to the NeighborNodes
    NeighborComm = set()
    for node in NeighborNodes:
        if CurrentResult[node] != c:
            NeighborComm.add(CurrentResult[node])
    return list(NeighborComm)


# Find all neighbor communities and neighbor of neighbor communities
def findPropagandizedNeighborComm(G, c, CurrentResult, height, res, path, S_bound, size):

    if height <= 0:
        return res

    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
    if size + len(CommunityNumToNodes[c]) > S_bound[1]: return res

    # save the neighbor communities in this height, format is "path,current comm"
    Neighbors = findAllNeighborsComm(G, c, CurrentResult)
    MergeCommListStr = []
    MergeCommList = []
    for com in Neighbors:
        if com not in path:
            tmp = ""
            for p in path:
                tmp += f"{p},"
            tmp += str(com)
            MergeCommListStr.append(tmp)
            MergeCommList.append(com)

    # If this height exits, append. Otherwise, create a new one
    if height in res:
        res[height] += MergeCommListStr
    elif MergeCommListStr:
        res[height] = MergeCommListStr

    # Search for the next level neighbors from this level neighbors one by one
    for com in MergeCommList:
        path.append(com)
        res = findPropagandizedNeighborComm(G, com, CurrentResult, height-1, res, path, S_bound, size + len(CommunityNumToNodes[com]))
        path.pop()

    return res


# Find all incoming edges to Community C
def findIncomingEdgesComm(G, c, CurrentResult, bio_flag):
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
    InEdges = []

    # Collect all incoming edges for the nodes in community c
    for node in CommunityNumToNodes[c]:
        tmp = ef.findIncomingEdges(G, node)
        for t in tmp:
            InEdges.append(t)

    # select the Incoming edges for the community c
    InEdgesComm = []
    OutNodes = set()
    for ele in list(InEdges):

        # ele[1] must be in c, because it is an incoming edge, end node must in c.
        if ele[0] not in CommunityNumToNodes[c]:

            # Only add one incoming edge for one outside node
            if bio_flag:
                if ele[0] not in OutNodes:
                    InEdgesComm.append(ele)
                    OutNodes.add(ele[0])

            # Add all incoming edges from outside
            else:
                InEdgesComm.append(ele)

    return InEdgesComm


# Find all outgoing edges from Community C
def findOutgoingEdgesComm(G, c, CurrentResult, bio_flag):
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
    OutEdges = []

    # Collect all outgoing edges for the nodes in community c
    for node in CommunityNumToNodes[c]:
        tmp = ef.findOutgoingEdges(G, node)
        for t in tmp:
            OutEdges.append(t)

    # select the Outgoing edges for the community c
    OutEdgesComm = []
    InNodes = set()
    for ele in list(OutEdges):

        # ele[1] must be in c, because it is an incoming edge, end node must in c.
        if ele[1] not in CommunityNumToNodes[c]:

            # Only add one outgoing edge for one inside node
            if bio_flag:
                if ele[0] not in InNodes:
                    OutEdgesComm.append(ele)
                    InNodes.add(ele[0])

            # Add all outgoing edges from inside
            else:
                OutEdgesComm.append(ele)

    return OutEdgesComm


# Add neighbor Community into current pending community
def addNeighborComm(CurrentResult, NeighborComm, PendingCommunity):
    CurrentResult_new = copy.deepcopy(CurrentResult)
    CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)

    # Check the NeighborComm, if it includes two neighbor communities, split it and merge them one by one.
    # If only one neighbor community, merge it directly.
    NeighborComms = NeighborComm.split(',')

    for tmp in NeighborComms:

        # update the nodes in neighbor Community to the pending community
        for node in CommunityNumToNodes[tmp]:
            CurrentResult_new[node] = PendingCommunity

    return CurrentResult_new


# Check loop caused by the current community c, if there is a loop, drop this try and back tracking to the last level.
def checkLoopComm(G, c, CurrentResult, bio_flag):
    InEdges = findIncomingEdgesComm(G, c, CurrentResult, bio_flag)
    OutEdges = findOutgoingEdgesComm(G, c, CurrentResult, bio_flag)

    # Find all communities provide incoming edges to community c
    InEdgesComm = set()
    for edge in InEdges:
        InEdgesComm.add(CurrentResult[edge[0]])

    # Find all communities provide outgoing edges from community c
    OutEdgesComm = set()
    for edge in OutEdges:
        OutEdgesComm.add(CurrentResult[edge[1]])

    # Compare InEdgesComm and OutEdgesComm, if they have same community b, that means loop between b and c.
    # Calculate the total number of cycles and return it.
    LoopComm = OutEdgesComm.intersection(InEdgesComm)

    return len(LoopComm)


# Check and find the worst case in PendingCommunities
# There won't be any cycle when we get into this function, because we will not allow a community make cycles during the
# community enlarge procedure. Every time when we try to run this function, the current graph should not have any cycle between communities.
def findWorstCommunity(G, PendingCommunities, CurrentResult, bio_flag):
    maxVal = 0
    maxKey = ''
    maxEdges = 0
    for key in PendingCommunities:

        # update the worst case when a community has bigger value
        if PendingCommunities[key] > maxVal:
            maxKey = key
            maxEdges = len(findIncomingEdgesComm(G, key, CurrentResult, bio_flag)) + len(findOutgoingEdgesComm(G, key, CurrentResult, bio_flag))

        # If the number of unmet constraints is equal, choose the one has more edges connected
        if PendingCommunities[key] == maxVal:
            if len(findIncomingEdgesComm(G, key, CurrentResult, bio_flag)) + len(findOutgoingEdgesComm(G, key, CurrentResult,bio_flag)) > maxEdges:
                maxKey = key
                maxEdges = len(findIncomingEdgesComm(G, key, CurrentResult, bio_flag)) + len(findOutgoingEdgesComm(G, key, CurrentResult, bio_flag))
    return maxKey


# Find the communities that cannot meet all constraints, if there is no pending community exists, return -1, else return its community number
def findPendingCommunities(G, result, constraint, bio_flag):
    PendingCommunities = {}
    for key in result:
        res = checkInOutComm(G, key, constraint, result, bio_flag) + checkLoopComm(G, key, result, bio_flag)
        if res != 0:
            PendingCommunities[key] = res
    return PendingCommunities


# Find the next community or communities to merge
def findMergeCommunities(G, result, constraint, bio_flag):
    MergeCommunities = {}
    CommunityNumToNodes = uf.mapCommunityToNodes(result)

    # Calculate the rewards for each community as the merging center
    for Comm in CommunityNumToNodes:
        MergeCommunities[Comm] = len(CommunityNumToNodes[Comm]) + sum(constraint) - len(findIncomingEdgesComm(G, Comm, result, bio_flag)) - len(findOutgoingEdgesComm(G, Comm, result, bio_flag))

    # Sort
    tmp = sorted(MergeCommunities.items(), key=lambda x: (x[1], x[0]), reverse=True)
    MergeCommunities = dict(tmp)

    return MergeCommunities