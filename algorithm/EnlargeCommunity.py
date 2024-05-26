import InitiateFunctions as inf
import CalculationFunctions as calf
import json
import csv
import NodeFunctions as nf
import InOutFunctions as iof
import collections
import EdgeColoring as eco
import CommunityFunctions as ccf
import copy
import UpdateFunctions as uf


def getUnNeighborRewards(residualComm, CommunityNumToNodes, NodeNum, S_bound, rewards, CommPath, Result, CenterCommunity, constraint, bio_flag, G, height, timestep):
    # force to escape from the current recursion if we meet the max height to search
    if height <= 0 or timestep < 0:
        return timestep, rewards

    # Search for the next level
    for c in residualComm:
        if timestep <= 0:
            break
        if (c not in CommPath) and (NodeNum + len(CommunityNumToNodes[c]) <= S_bound[1]):

            # create the comm group as the key if we find more than 1 comm can be merged
            path_sorted = sorted(CommPath + [c])
            tmp = ""
            for p in path_sorted[:-1]:
                tmp += f"{p},"
            tmp += str(path_sorted[-1])

            r = calf.calculateRewardComm(G, c, CenterCommunity, Result, constraint, bio_flag)
            if r >= 0:
                rewards[tmp] = r
                timestep, _ = getUnNeighborRewards(residualComm, CommunityNumToNodes, NodeNum + len(CommunityNumToNodes[c]), S_bound, rewards, path_sorted, Result,
                             CenterCommunity, constraint, bio_flag, G, height-1, timestep-1)


    return timestep, rewards


# propagation checking stop after the given height
# height2 is used for combining the unconnected cells, stop in a limited searching height.
def prepareCommOrder(G, CenterCommunity, CurrentResult, constraint, bio_flag, height, height2, S_bound, ub, path_set, count=0):

    rewards = {}
    flag = True
    # Initiate the values we will return
    CurrentResult_new = copy.deepcopy(CurrentResult)

    # No more neighbors can be added into this center community. So try the communities without connected edges
    if count == 2:
        flag = False

        # return without merging un-neighbor nodes
        # return {}, CurrentResult_new, path_set, flag

        # try merging un-neighbor nodes
        CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
        if CenterCommunity in CommunityNumToNodes and len(CommunityNumToNodes[CenterCommunity]) < S_bound[1]:

            # Get all the left communities with fewer inside nodes than upperbound. That means they still have space to merge.
            residualComm = []
            for c in CommunityNumToNodes:
                if c != CenterCommunity and len(CommunityNumToNodes[c]) + len(CommunityNumToNodes[CenterCommunity]) <= S_bound[1]:
                    residualComm.append(c)
            NodeNum = len(CommunityNumToNodes[CenterCommunity])

            # merge communities as big as possible every time, upper bound for search timestep is set to 100.
            CommPath = [CenterCommunity]
            timestep, rewards = getUnNeighborRewards(residualComm, CommunityNumToNodes, NodeNum, S_bound, rewards, CommPath, CurrentResult_new,
                                                     CenterCommunity, constraint, bio_flag, G, height2, 100)
    else:

        # calculate the rewards provided by all neighbor communities and the n-height neighbors of the neighbors if we add them into the current community
        # This procedure is called propagation checking
        CommunityNumToNodes = uf.mapCommunityToNodes(CurrentResult)
        PropagandizedNeighborComm, rewards, path_set = ccf.findPropagateNeighborComm(G, CenterCommunity, CurrentResult, height-1, {height: CenterCommunity},
                                                                               [CenterCommunity], S_bound, len(CommunityNumToNodes[CenterCommunity]),
                                                                               [0], {}, constraint, bio_flag, path_set, ub)

    # find the community provides the highest reward, sort this rewards dictionary first and try them in the order
    tmp = sorted(rewards.items(), key=lambda x: (x[1], len(x[0]), x[0]), reverse=True)
    rewards_new = dict(tmp)

    return rewards_new, CurrentResult_new, path_set, flag


# Work for verification
# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving the highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, Community, S_bounds, ConstraintType, timestep, constraint, loop_free, CurrentResult, bio_flag, ub, height=0, height2=0):
    VerifyFlag, ErrorLog = False, {}

    rewards_new, CurrentResult_new, path_set, _ = prepareCommOrder(G, Community, CurrentResult, constraint, bio_flag, height, 0, S_bounds, ub, set())

    # start the middle part of backtracking
    for c in rewards_new:
        if timestep < 0:
            return CurrentResult_new, VerifyFlag, {f"Community {Community} cannot be solved! Try increasing timestep"}, timestep
        else:
            timestep -= 1

        # Update the current verify result after adding the neighbor community
        # Here we create a new variable CurrentResult_updated, because we can use CurrentResult_new as the original data in the final stage of backtracking
        CurrentResult_updated = ccf.addNeighborComm(CurrentResult_new, c, Community)
        # print("Merge: ", c)

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
                    return CurrentResult_updated, True, {}, timestep

                # else, check the next one
                Community = ccf.findWorstCommunity(G, PendingCommunities, CurrentResult_updated, bio_flag)
                # print("Start new pending community: ", Community)
                CurrentResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, Community, S_bounds, ConstraintType, timestep,
                                                                             constraint, loop_free, CurrentResult_updated, bio_flag, ub, height,height2)
        if VerifyFlag:
            return CurrentResult_updated, VerifyFlag, ErrorLog, timestep
    return CurrentResult_new, VerifyFlag, {f"Community {Community} cannot be solved! Try increasing ub, height, or height2"}, timestep


# In this function, we only provide the list of as-center-to-be-merged communities, in order of calculated center-merging rewards.
def prepareMerge(Neighborflag, totalNum, count, SearchStep, MergeResult, attempt_range, Result, constraint, bio_flag, G, S_bounds):

    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    ll = len(CommunityNumToNodes)
    MergeCommunities = {}

    # If no change has been done to the MergeResult after the checking above, we should change a different way to order the to-be-merged communities.
    # We can skip this attempt because we have known the answer yet.
    # if un-Neighbor nodes are also checked, we should skip from the current attempt.
    if not Neighborflag:
        if attempt_range[1] > attempt_range[0]:
            attempt_range[1] -= 1
            print(f"Attempt {attempt_range[1]}: ", f"{ll} cells in total. ", "Try another way to merge!")

            # Time to quit
            if attempt_range[1] <= attempt_range[0]:
                print("No more attempts left!")
                return MergeCommunities, totalNum, count, SearchStep, attempt_range, MergeResult
            else:
                MergeResult = copy.deepcopy(Result)
                ll = len(uf.mapCommunityToNodes(MergeResult))
                count = 1
                SearchStep += 1

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
        MergeCommunities = ccf.changeOrder(MergeCommunities, SearchStep)
    else:
        count = 1
        totalNum = ll

    # Find all possible to-be-merged communities and sort them with rewards. Scan them in this order.
    # SearchStep determine the order of communities to be merged
    # If SearchStep == 1, all communities will be in the to-be-merged list.
    # For the 1st attempt, we don't change the order of reward list in each merge round.
    # A merge round means go through the while loop in tryMerge()
    # For the n-th attempt, SearchStep will be set as n, in each merge round, we will set a random seed as n to order the merge list.
    if count == 1:
        MergeCommunities = ccf.findMergeCommunities(G, MergeResult, constraint, bio_flag, SearchStep)

    return MergeCommunities, totalNum, count, SearchStep, attempt_range, MergeResult


# If the current merge result is going to be added to the solution list, rename the key can make reduce more duplication
def renameKey(OldResult):
    NewResult = {}
    CommunityNumToNodes = uf.mapCommunityToNodes(OldResult)
    for key in CommunityNumToNodes:
        val = CommunityNumToNodes[key]
        # Assign the name of current community as the first element in val.
        # The first element in val is also the smallest value in the current community, because we create CommunityNumToNodes by ascending order
        for node in val:
            NewResult[node] = val[0]
    return NewResult


def tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free, Result, attempt_range, ub):
    totalNum = 0
    count = 1
    MergeResultList = [MergeResult]
    SearchStep = attempt_range[0]
    Neighborflag = True

    # There are 2 possible conditions to return back
    # 1. meet target n constraint
    # 2. meet time constraint
    # SearchStep determine the order of communities to be merged
    while timestep >= 0:
        path_set = set()
        print(totalNum, len(uf.mapCommunityToNodes(MergeResult)), count, timestep, Neighborflag)
        MergeCommunities, totalNum, count, SearchStep, attempt_range, MergeResult = prepareMerge(Neighborflag, totalNum, count, SearchStep, MergeResult, attempt_range, Result, constraint, bio_flag, G, S_bounds)

        if attempt_range[1] <= attempt_range[0]:
            break

        # RewardCounter shows how many communities we have tried.
        # Try to merge the communities in the order of MergeCommunities
        RewardCounter = 0
        for Community in MergeCommunities:

            # Find all neighbor communities around the chosen community.
            # And get the sorted rewards dictionary for all the propagated neighbor communities
            rewards_sorted, _, path_set, Neighborflag = prepareCommOrder(G, Community, MergeResult, constraint, bio_flag, height, height2, S_bounds, ub, path_set, count)
            RewardCounter += 1
            if RewardCounter % 1000 == 0:
                print(f"Have tried to merge {RewardCounter}th community candidate, now we have {len(uf.mapCommunityToNodes(MergeResult))} communities.")

            for key in rewards_sorted:

                # Merge the neighbor community providing the highest reward currently
                MergeResult_updated = ccf.addNeighborComm(MergeResult, key, Community)

                # If size is bigger than upper bound, change to another community path, and MergeResult_update doesn't need to be changed back.
                # Next time it will be assigned with acceptable result from MergeResult. MergeResult is not modified until meet all constraints.
                if ccf.checkSize(MergeResult_updated, Community) > S_bounds[1]:
                    continue

                # If current merge operation (added one neighbor community to current one in the last level) can be accepted,
                # update the current merge result to MergeResult and break the loop, go to the next merge community.
                # checkloop = 0 and checkInOutComm = 0 means the current community meets all the constraints
                if ((loop_free and ccf.checkLoopComm(G, Community, MergeResult_updated, bio_flag) == 0) or not loop_free) and \
                        ccf.checkInOutComm(G, Community, constraint, MergeResult_updated, bio_flag) == 0:
                    MergeResult_updated = renameKey(MergeResult_updated)
                    MergeResultList.append(MergeResult_updated)
                    MergeResult = MergeResult_updated
                    break

        # After leaving from the for loop, we may have a successful merge or not.
        # Keep checking until all communities are checked.
        timestep -= 1
        # ll = len(uf.mapCommunityToNodes(MergeResult))
        # print(f"attempt {attempts}: ", f"{timestep} timesteps left, ", f"{ll} cells in solution now.")

    ll = len(uf.mapCommunityToNodes(MergeResult))
    return MergeResultList, MergeResult, ll


# Remove duplication merge solution in the list
# Then sort the un-duplicated solution list
# Save the list as json and csv
def sortAndSaveMergeResultList(S_bounds, out_path, constraint, MergeResultList, MergeResult, attempt_range, bio_flag):

    # Last MergeResult was not added to the list, add it now.
    # reduce duplication in the list
    MergeResultList.append(MergeResult)
    MergeResultList = [dict(t) for t in set([tuple(d.items()) for d in MergeResultList])]

    # collect length of merge result list.
    d = {}
    for i in range(len(MergeResultList)):
        # calculate the number of cells for each merge result now
        ll = len(collections.Counter(list(MergeResultList[i].values())))
        d[i] = ll

    # Sort the given dictionary, tmp is a dictionary with key = index in MergeResult, value = length of that merge result
    print(f"{len(d)} possible solutions to be checked for edge coloring assignment!")
    tmp = sorted(d.items(), key=lambda x: (x[1], x[0], x[0] == 0), reverse=False)
    tmp = dict(tmp)

    # save the sorted merge result list to a json file
    new_d = []
    if not bio_flag:
        for i in tmp:
            new_d.append([tmp[i], MergeResultList[i]])
            break
        return MergeResultList, tmp, new_d

    with open(f"{out_path}/merge_result_list_{S_bounds[1]}_{constraint[0]}_{attempt_range}.csv", "w", newline="") as csv_file:
        fieldnames = ["Total Number of Comms", "Solution"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in tmp:
            ComSol = uf.mapCommunityToNodes(MergeResultList[i])
            new_d.append([len(ComSol), MergeResultList[i]])
            info_row = {"Total Number of Comms": len(ComSol), "Solution": ComSol}
            writer.writerow(info_row)

    # save the sorted merge result list to a json file
    with open(f"{out_path}/merge_result_list_{S_bounds[1]}_{constraint[0]}_{attempt_range}.json", "w") as json_file:
        json.dump(new_d, json_file)

    return MergeResultList, tmp, new_d


# Enlarge Communities in the Merge stage using height level neighbor propagation checking. (every time try to merge multiple communities)
def enlargeCommunityMerge(G, S_bounds, out_path, constraint, loop_free, timestep, Result, target_n, bio_flag, height, height2, attempt_range, ub):

    Result = renameKey(Result)
    MergeResult = copy.deepcopy(Result)
    attempt_range_original = copy.deepcopy(attempt_range)
    MergeResultList, MergeResult, ll = tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free, Result,
                                                attempt_range, ub)

    MergeResultList, tmp, d_new = sortAndSaveMergeResultList(S_bounds, out_path, constraint, MergeResultList, MergeResult, attempt_range_original, bio_flag)
    MergeResult = d_new[0][1]

    # If the current number of communities is bigger than what we expected (target_n), return False
    if len(uf.mapCommunityToNodes(MergeResult)) <= target_n:
        return MergeResult, True, {}
    else:
        return MergeResult, False, {"No more attempts"}


# Merging for Chris group: Every time when we decide to merge, do edge-coloring assignment first. If it fails, drop it and try next one.
def enlargeCommunityMerge_chris(G, S_bounds, out_path, constraint, loop_free, timestep, Result, target_n, bio_flag, height, height2, DAG_original, ColorOptions, attempt_range, ub):
    DAG = copy.deepcopy(DAG_original)
    MergeResult = copy.deepcopy(Result)
    MergeResult = renameKey(MergeResult)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    MergeResultList, MergeResult, ll = tryMerge(G, MergeResult, constraint, bio_flag, height, height2, S_bounds, timestep, loop_free, Result,
                                                attempt_range, ub)

    MergeResultList, tmp, d_new = sortAndSaveMergeResultList(S_bounds, out_path, constraint, MergeResultList, MergeResult, attempt_range, bio_flag)

    # If we can find a solution with all edge colored correctly, then return the merge result. Otherwise, try another one in the merge result list
    currentlengh = len(CommunityNumToNodes)
    for i in tmp:
        res = MergeResultList[i]
        CommunityNumToNodes = uf.mapCommunityToNodes(res)

        if currentlengh != len(CommunityNumToNodes):
            currentlengh = len(CommunityNumToNodes)
            print(f"Now check the result with {currentlengh} communities")
        ColorFlag, DAG, _, _ = eco.ColorAssignment(res, CommunityNumToNodes, G, DAG, bio_flag, ColorOptions, 5000)
        if ColorFlag:
            print("Edges can be colored correctly!")

            if len(CommunityNumToNodes) <= target_n:
                return res, True, {}, ColorFlag, DAG
            elif timestep < 0:
                return res, False, {"Time runs out"}, ColorFlag, DAG
            else:
                return res, False, {f"{attempt_range[1] - attempt_range[0]} attempts runs out"}, ColorFlag, DAG

    # If all the results cannot give correct edge coloring assignment
    print("No solution can be found")
    return {}, False, {"No solution can satisfy our edge coloring assignment!"}, False, DAG
