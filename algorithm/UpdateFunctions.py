import collections
import copy


# update community numbers, and return a dictionary with key=community number, and value=[nodes, nodes, ...]
def updateCommunityNum(CurrentResult):
    CurrentResult_new = copy.deepcopy(CurrentResult)

    # Sort the dictionary by int(key)
    tmp = sorted(CurrentResult_new.items(), key=lambda x: int(x[0]))
    CurrentResult_new = dict(tmp)

    CommunityNumToNodes = mapCommunityToNodes(CurrentResult_new)
    # update community numbers start from 1
    i = 1
    NewCommunityNumToNodes = {}
    for key in CommunityNumToNodes:
        NewCommunityNumToNodes[i] = CommunityNumToNodes[key]

        # update the new community numbers for each node in CurrentResult
        for node in CommunityNumToNodes[key]:
            CurrentResult_new[node] = i
        i += 1

    return NewCommunityNumToNodes, CurrentResult_new


# map community to nodes
def mapCommunityToNodes(CurrentResult):
    CommunityNumToNodes = collections.defaultdict(list)

    # key here is the community number
    for key in CurrentResult:
        CommunityNumToNodes[CurrentResult[key]].append(key)

    return CommunityNumToNodes