import collections

# update community numbers, and return a dictionary with key=community number, and value=[nodes, nodes, ...]
def updateCommunityNum(CurrentVerifyResult):
    print(CurrentVerifyResult)

    CommunityNumToNodes = mapCommunityToNodes(CurrentVerifyResult)
    # update community numbers start from 1
    i = 1
    NewCommunityNumToNodes = {}
    for key in CommunityNumToNodes:
        NewCommunityNumToNodes[i] = CommunityNumToNodes[key]

        # update the new community numbers for each node in CurrentVerifyResult
        for node in CommunityNumToNodes[key]:
            CurrentVerifyResult[node] = i
        i += 1

    print(CurrentVerifyResult)
    return NewCommunityNumToNodes, CurrentVerifyResult


# map community to nodes
def mapCommunityToNodes(CurrentVerifyResult):
    CommunityNumToNodes = collections.defaultdict(list)

    # key here is the community number
    for key in CurrentVerifyResult:
        CommunityNumToNodes[CurrentVerifyResult[key]].append(key)

    return CommunityNumToNodes