import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import InOutFunctions as iof
import CommunityFunctions as ccf
import copy


def prepareNeighborOrder(G, Community, CurrentResult, constraint):

    # Initiate the values we will return
    CurrentResult_new = copy.deepcopy(CurrentResult)
    VerifyFlag = True
    ErrorLog = {}

    # calculate the rewards provided by all neighbor communities if we add them into the current community
    NeighborComm = ccf.findAllNeighborsComm(G, Community, CurrentResult)
    rewards = {}
    for c in NeighborComm:
        rewards[c] = calf.calculateRewardComm(G, c, Community, CurrentResult, constraint)

    # find the community provides the highest reward, sort this rewards dictionary first and try them in the order
    tmp = sorted(rewards.items(), key=lambda x: x[1], reverse=True)
    rewards_new = dict(tmp)

    return rewards_new, CurrentResult_new

# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving the highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, Community, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, CurrentResult):

    # Return to the last level if it arrives to the size constraints, time constraint or current community meets all constraints
    if ccf.checkSize(CurrentResult, Community) > S_bounds[1]:
        return CurrentResult, False, {Community}, timestep
    if timestep < 0:
        return CurrentResult, False, {"Time runs out"}, timestep

    # When the current community meets all constraints, transfer to the next one
    if ccf.checkLoopComm(G, Community, CurrentResult) == 0 and ccf.checkInOutComm(G, Community, constraint, CurrentResult) == 0:

        # Find other pending communities
        PendingCommunities = ccf.findPendingCommunities(G, CurrentResult, constraint)

        # If no other pending communities, return current result.
        if len(PendingCommunities) == 0:
            return CurrentResult, True, {}, timestep

        # If there are still some pending communities, find the worst one and solve it next.
        Community = ccf.findWorstCommunity(G, PendingCommunities, CurrentResult)
        print("PendingCommunities: ", PendingCommunities)
        print("Community: ", Community)

        # Start solving the new pending community
        CurrentResult, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, Community, S_bounds, ConstraintType,
                                                                               constraint, loop_free, priority, timestep-1, CurrentResult)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the last level and try the other neighbor nodes
        if VerifyFlag:
            return CurrentResult, True, {}, timestep
        else:
            return CurrentResult, False, {Community}, timestep

    rewards_new, CurrentResult_new = prepareNeighborOrder(G, Community, CurrentResult, constraint)

    # start the middle part of backtracking
    for c in rewards_new:
        if timestep % 10000 == 0:
            print("Rewards: ", c, rewards_new[c])
            print("Timestep: ", timestep)

        # Update the current verify result after adding the neighbor community
        # Here we create a new variable C_updated, because we can use C_new as the original data in the 3rd stage of backtracking
        CurrentResult_updated = ccf.addNeighborComm(CurrentResult_new, c, Community)
        CurrentResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, Community, S_bounds, ConstraintType,
                                                                         constraint, loop_free, priority, timestep-1,  CurrentResult_updated)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the scenario before adding the current neighbor node
        if VerifyFlag:
            return CurrentResult_updated, True, {}, timestep
        elif timestep < 0:
            return CurrentResult_new, False, {"Time runs out"}, timestep

    return CurrentResult_new, VerifyFlag, ErrorLog, timestep


# Enlarge Communities in the Merge stage
def enlargeCommunityMerge(G, Community, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, MergeResult, target_n):

    # There are 3 possible conditions to return back
    # 1. meet size constraint
    # 2. meet time constraint
    # 3. merge can be accepted
    # 3-1. if it also target n constraint, return the current merge result as the final solution
    # 3-2. if not, keep merge the next community

    # If size is bigger than upper bound, return false
    if ccf.checkSize(MergeResult, Community) > S_bounds[1]:
        return MergeResult, False, {1, Community}, timestep

    # If current merge operation (added one neighbor community to current one in the last level) can be accepted, check target n
    if ccf.checkLoopComm(G, Community, MergeResult) == 0 and ccf.checkInOutComm(G, Community, constraint, MergeResult) == 0:

        # If target n is achieved, return true
        CurrentCommNum = len(set(MergeResult.values()))
        if CurrentCommNum <= target_n:
            return MergeResult, True, {"Merge succeed!"}, timestep

        # If target n is not achieved, but current merge can be accepted, then we try to merge another community to current one
        Community = ccf.findNextMergeCommunity(G, MergeResult, constraint)
        print("This merge operation passed!")
        print("Now try merging next community: ", Community)
        MergeResult, MergeFlag, MergeErrorLog, timestep = enlargeCommunityMerge(G_primitive, Community, S_bounds, ConstraintType, constraint,
                                                                      loop_free, priority, timestep-1, MergeResult, target_n)

        # After merging other communities, if MergeFlag == True, we can directly return the current merge result as the final result
        if MergeFlag:
            return MergeResult, True, {"Merge succeed!"}, timestep

        # If it is False, that means all the possible merge operation for the given community (after merging this neighbor community)
        # in the current graph failed
        # So go back to the last level and try to merge other communities into the current one.
        else:
            return MergeResult, False, {Community}, timestep

    # If the current merge operation cannot be accepted, return back to the last level
    else:
        return MergeResult, False, {Community}, timestep

    # If timestep is achieved, return false
    if timestep < 0:
        return MergeResult, False, {"Time runs out"}, timestep

    # Start to merge neighbor communities to the current chosen merging community. Try all neighbor communities until it meets any condition above
    rewards_new, MergeResult_new = prepareNeighborOrder(G, Community, MergeResult, constraint)




    # Here, we are not like verificaiton enlargecommunity part, we can accept all MergeResult if the number of total communities is decreasing.




