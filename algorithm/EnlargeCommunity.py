import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import InOutFunctions as iof
import collections
import EdgeColoring as eco
import CommunityFunctions as ccf
import copy
import UpdateFunctions as uf


def getUnNeighborRewards(residualComm, CommunityNumToNodes, GateNum, S_bound, rewards, CommPath, Result, CenterCommunity, constraint, bio_flag, G, height):

    # force to escape from the current recursion if we meet the max height to search
    if height <= 0 or GateNum >= S_bound[1]:
        return rewards

    # Search for the next level
    for c in residualComm:
        if c not in CommPath and GateNum + len(CommunityNumToNodes[c]) <= S_bound[1]:

            # create the comm group as the key if we find more than 1 comm can be merged
            path_sorted = sorted(CommPath + [c])
            tmp = ""
            for p in path_sorted[:-1]:
                tmp += f"{p},"
            tmp += str(path_sorted[-1])

            r = calf.calculateRewardComm(G, c, CenterCommunity, Result, constraint, bio_flag)
            if r >= -1:
                rewards[tmp] = r
                getUnNeighborRewards(residualComm, CommunityNumToNodes, GateNum + len(CommunityNumToNodes[c]), S_bound, rewards, path_sorted, Result,
                                 CenterCommunity, constraint, bio_flag, G, height-1)
    return rewards


# propaganda checking stop after the given height
# height2 is used for combining the unconnected cells, stop in a limited searching height.
def prepareNeighborOrder(G, CenterCommunity, CurrentResult, constraint, bio_flag, height, height2, S_bound, ub, path_set, count=0):

    rewards = {}
    # Initiate the values we will return
    CurrentResult_new = copy.deepcopy(CurrentResult)

    # No more neighbors can be added into this centercommunity. So try the communities without connected edges
    if count == 2:
        CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
        if CenterCommunity in CommunityNumToNodes and len(CommunityNumToNodes[CenterCommunity]) < S_bound[1]:

            # Get all the left communities with less gates inside than upperbound. That means they still have space to merge.
            residualComm = []
            for c in CommunityNumToNodes:
                if c != CenterCommunity and len(CommunityNumToNodes[c]) + len(CommunityNumToNodes[CenterCommunity]) <= S_bound[1]:
                    residualComm.append(c)
            GateNum = len(CommunityNumToNodes[CenterCommunity])

            # merge communities as big as possible every time
            CommPath = [CenterCommunity]
            rewards = getUnNeighborRewards(residualComm, CommunityNumToNodes, GateNum, S_bound, rewards, CommPath, CurrentResult_new, CenterCommunity,
                                           constraint, bio_flag, G, height2)
    else:

        # calculate the rewards provided by all neighbor communities and the n-height neighbors of the neighbors if we add them into the current community
        # This procedure is called propaganda checking
        CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
        PropagandizedNeighborComm, rewards, path_set = ccf.findPropagandizedNeighborComm(G, CenterCommunity, CurrentResult, height-1, {height: CenterCommunity},
                                                                               [CenterCommunity], S_bound, len(CommunityNumToNodes[CenterCommunity]),
                                                                               [0], {}, constraint, bio_flag, path_set, ub)

    # find the community provides the highest reward, sort this rewards dictionary first and try them in the order
    tmp = sorted(rewards.items(), key=lambda x: (x[1], len(x[0]), x[0]), reverse=True)
    rewards_new = dict(tmp)

    return rewards_new, CurrentResult_new, path_set


# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving the highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, Community, S_bounds, ConstraintType, constraint, loop_free, priority, CurrentResult, bio_flag, ub, height=0, height2=0):
    VerifyFlag, ErrorLog = False, {}

    rewards_new, CurrentResult_new, path_set = prepareNeighborOrder(G, Community, CurrentResult, constraint, bio_flag, height, 0, S_bounds, ub, set())

    # start the middle part of backtracking
    for c in rewards_new:

        # Update the current verify result after adding the neighbor community
        # Here we create a new variable CurrentResult_updated, because we can use CurrentResult_new as the original data in the final stage of backtracking
        CurrentResult_updated = ccf.addNeighborComm(CurrentResult_new, c, Community)
        print("Merge: ", c)

        # Return to the last level if it arrives to the size constraints, time constraint or current community meets all constraints
        if ccf.checkSize(CurrentResult_updated, Community) > S_bounds[1]:
            continue

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the scenario before adding the current neighbor node
        if (loop_free and ccf.checkLoopComm(G, Community, CurrentResult_updated, bio_flag) == 0) or not loop_free:
            if ccf.checkInOutComm(G, Community, constraint, CurrentResult_updated, bio_flag) == 0:

                # Find other pending communities
                PendingCommunities = ccf.findPendingCommunities(G, CurrentResult_updated, constraint, bio_flag)

                # If no other pending communities, return current result.
                if len(PendingCommunities) == 0:
                    return CurrentResult_updated, True, {}

                # else, check the next one
                Community = ccf.findWorstCommunity(G, PendingCommunities, CurrentResult_updated, bio_flag)
                print("Start new pending community: ", Community)
                CurrentResult_updated, VerifyFlag, ErrorLog = enlargeCommunity(G, Community, S_bounds, ConstraintType,
                                                                             constraint, loop_free, priority,  CurrentResult_updated, bio_flag, ub, height)
        if VerifyFlag:
            return CurrentResult_updated, VerifyFlag, ErrorLog
    return CurrentResult_new, VerifyFlag, {f"Community {Community} cannot be solved!"}


def prepareMerge(totalNum, count, SearchStep, MergeResult, attempts, Result, constraint, bio_flag, G, S_bounds, ub):

    initial_flag = False
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    ll = len(CommunityNumToNodes)
    MergeCommunities = {}

    # assign rewards for each community before any operation, use these rewards to set the order of merging center for un-neighbor merging.
    if totalNum == ll:
        count += 1
        for c in CommunityNumToNodes:
            if len(CommunityNumToNodes[c]) < S_bounds[1]:
                MergeCommunities[c] = len(CommunityNumToNodes[c]) + sum(constraint) - len(ccf.findIncomingEdgesComm(G, c, MergeResult, bio_flag)) -\
                                      len(ccf.findOutgoingEdgesComm(G, c, MergeResult, bio_flag))
        # Sort
        tmp = sorted(MergeCommunities.items(), key=lambda x: (x[1], x[0]), reverse=True)
        MergeCommunities = dict(tmp)
    else:
        count = 1
        totalNum = ll

    # print(f"There are {attempts} attempts left: Current number of communities: {ll}!")
    # print(f"Current number of communities: {totalNum}, stay in this number for {count} times")
    # If no change has been done to the MergeResult after this loop, then it will go to the same merging solution as the SearchStep=1.
    # We can skip this attempt because we have known the answer yet.
    if count == 3:
        if attempts > 0:
            totalNum = len(uf.mapCommunityToNodes(MergeResult))
            attempts -= 1
            if (attempts+1) % 100 == 0:
                print(f"There are {attempts} attempts left. ", f"{totalNum} cells in total. ", "Try another way to merge!")
            if attempts <= 0:
                print("No more attempts left!")
            else:
                MergeResult = copy.deepcopy(Result)
                count = 1
                SearchStep += 1
                initial_flag = True

    if count == 1:
        # Find all possible to-be-merged communities and sort them with rewards. Scan them in this order.
        # In the initial step, searchstep will determine the communities to be merged in this step.
        # if SearchStep == 1, all communities will be in the to-be-merged list, if it is 5, findMergeCommunities() will only return 5th, 10th, 15th,...
        # (products of 5) elements in the original dictionary.
        MergeCommunities = ccf.findMergeCommunities(G, MergeResult, constraint, bio_flag, initial_flag, SearchStep)

    return MergeCommunities, ub, totalNum, count, SearchStep, attempts, MergeResult


def tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free,target_n, Result, attempts, ub):
    totalNum = 0
    count = 1
    MergeResultList = []
    SearchStep = 1
    ll = len(uf.mapCommunityToNodes(MergeResult))

    # There are 2 possible conditions to return back
    # 1. meet target n constraint
    # 2. meet time constraint
    while timestep >= 0 and attempts > 0:
        path_set = set()
        MergeCommunities, ub, totalNum, count, SearchStep, attempts, MergeResult = prepareMerge(totalNum, count, SearchStep, MergeResult, attempts, Result, constraint, bio_flag, G, S_bounds, ub)

        # Try to merge the communities in the order of MergeCommunities
        for Community in MergeCommunities:
            # Find all neighbor communities around the chosen community.
            # And get the sorted rewards dictionary for all the neighbor communities
            rewards_sorted, _, path_set = prepareNeighborOrder(G, Community, MergeResult, constraint, bio_flag, height, height2, S_bounds, ub, path_set, count)

            for key in rewards_sorted:

                # Merge the neighbor community providing the highest reward currently
                MergeResult_updated = ccf.addNeighborComm(MergeResult, key, Community)

                # If size is bigger than upper bound, change to another community
                if ccf.checkSize(MergeResult_updated, Community) > S_bounds[1]:
                    continue

                # If current merge operation (added one neighbor community to current one in the last level) can be accepted,
                # update the current merge result to MergeResult and break the loop, go to the next merge community.
                # checkloop = 0 and checkInOutComm = 0 means the current community meets all the constraints
                if ((loop_free and ccf.checkLoopComm(G, Community, MergeResult_updated, bio_flag) == 0) or not loop_free) and \
                        ccf.checkInOutComm(G, Community, constraint, MergeResult_updated, bio_flag) == 0:
                    MergeResultList.append(MergeResult_updated)
                    MergeResult = MergeResult_updated
                    break

        timestep -= 1
        # After leaving from the for loop, we may have a successful merge or not.
        # Keep checking until all communities are checked.

        ll = len(uf.mapCommunityToNodes(MergeResult))
    return MergeResultList, MergeResult, ll


# Merging Method 1: Enlarge Communities in the Merge stage using two level neighbor propaganda checking. (every time merge one or two communities)
def enlargeCommunityMerge(G, S_bounds, constraint, loop_free, priority, timestep, Result, target_n, bio_flag, height, height2, attempts, ub):
    MergeResult = copy.deepcopy(Result)
    MergeResultList, MergeResult, ll = tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free,target_n, Result, attempts, ub)

    # reduce duplication in the list
    MergeResultList = [dict(t) for t in set([tuple(d.items()) for d in MergeResultList])]
    minval = ll
    for res in MergeResultList:
        tmp = uf.mapCommunityToNodes(res)
        if len(tmp) < minval:
            minval = len(tmp)
            MergeResult = res

    if len(uf.mapCommunityToNodes(MergeResult)) <= target_n:
        return MergeResult, True, {}
    else:
        return MergeResult, False, {"Time runs out"}


# Merging for Chris group: Every time when we decide to merge, do edge-coloring assignment first. If it fails, drop it and try next one.
def enlargeCommunityMerge_chris(G, S_bounds, constraint, loop_free, timestep, Result, target_n, bio_flag, height, height2, DAG_original, ColorOptions, attempts, ub):
    DAG = copy.deepcopy(DAG_original)
    MergeResult = copy.deepcopy(Result)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    MergeResultList, MergeResult, ll = tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free, target_n, Result,
                                                attempts, ub)

    # reduce duplication in the list
    if len(MergeResult) != len(Result) or S_bounds[1] == 1:
        MergeResultList.append(MergeResult)
    MergeResultList = [dict(t) for t in set([tuple(d.items()) for d in MergeResultList])]

    # If edge coloring assignment failed, change to another community
    d = {}
    for i in range(len(MergeResultList)):

        # calculate the number of cells now
        ll = len(collections.Counter(list(MergeResultList[i].values())))
        if 60 < ll < 64:
            d[i] = ll


    # Sort the given dictionary
    print(f"{len(d)} possible solutions to be checked for edge coloring assignment!")
    tmp = sorted(d.items(), key=lambda x: (x[1], x[0]), reverse=False)
    tmp = dict(tmp)

    # If we can find a solution with all edge colored correctly, then return the merge result. Otherwise, try another one in the merge result list
    currentlengh = len(CommunityNumToNodes)
    for i in tmp:
        res = MergeResultList[i]
        CommunityNumToNodes = uf.mapCommunityToNodes(res)

        if currentlengh != len(CommunityNumToNodes):
            currentlengh = len(CommunityNumToNodes)
            print(f"Now check the result with {len(CommunityNumToNodes)} communities")
        ColorFlag, DAG = eco.ColorAssignment(res, CommunityNumToNodes, G, DAG, bio_flag, ColorOptions)
        if ColorFlag:
            print("Find solution can be colored correctly!")

            if len(CommunityNumToNodes) <= target_n:
                return res, True, {}, ColorFlag, DAG
            elif timestep < 0:
                return res, False, {"Time runs out"}, ColorFlag, DAG
            else:
                return res, False, {f"{attempts} attempts runs out"}, ColorFlag, DAG

    # If all the results cannot give correct edge coloring assignment
    print("No solution can be found")
    return {}, False, {"No solution can satisfy our edge coloring assignment!"}, False, DAG
