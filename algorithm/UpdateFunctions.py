import collections

# update community numbers, and return a dictionary with key=community number, and value=[nodes, nodes, ...]
def updateCommunityNum(CurrentVerifyResult):
    print(CurrentVerifyResult)
    CommunityNumToNodes = collections.defaultdict(list)

    # key here is the community number
    for key in CurrentVerifyResult:
        CommunityNumToNodes[CurrentVerifyResult[key]].append(key)

    # update community numbers start from 1
    i = 1
    NewCommunityNumToNodes = {}
    for key in CommunityNumToNodes:
        NewCommunityNumToNodes[i] = CommunityNumToNodes[key]

        # update the new community numbers for each node in CurrentVerifyResult
        for node in CommunityNumToNodes[key]:
            CurrentVerifyResult[node] = i
        i += 1

    print(CommunityNumToNodes)
    print(NewCommunityNumToNodes)
    print(CurrentVerifyResult)
    return NewCommunityNumToNodes, CurrentVerifyResult