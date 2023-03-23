import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import InOutFunctions as iof
import CommunityFunctions as ccf
import copy
import UpdateFunctions as uf


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
    if ((loop_free and ccf.checkLoopComm(G, Community, CurrentResult) == 0) or not loop_free) and ccf.checkInOutComm(G, Community, constraint, CurrentResult) == 0:

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
        if timestep % 100000 == 0:
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
def enlargeCommunityMerge(G, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, MergeResult, target_n):

    # There are 2 possible conditions to return back
    # 1. meet target n constraint
    # 2. meet time constraint
    while timestep >= 0 and len(uf.mapCommunityToNodes(MergeResult)) > target_n:
        print("Current number of communities", len(uf.mapCommunityToNodes(MergeResult)))

        # Find all possible to-be-merged communities and sort them with rewards. Scan them in this order.
        MergeCommunities = ccf.findMergeCommunities(G, MergeResult, constraint)

        # Try to merge the communities in the order of MergeCommunities
        for Community in MergeCommunities:

            print(MergeResult)

            # Find all neighbor communities around the chosen community.
            # And get the sorted rewards dictionary for all the neighbor communities
            rewards_sorted, _ = prepareNeighborOrder(G, Community, MergeResult, constraint)

            for key in rewards_sorted:

                # Merge the neighbor community provide the current highest reward
                MergeResult_updated = ccf.addNeighborComm(MergeResult, key, Community)

                # If size is bigger than upper bound, change to another community
                if ccf.checkSize(MergeResult_updated, Community) > S_bounds[1]:
                    continue

                # If current merge operation (added one neighbor community to current one in the last level) can be accepted,
                # update the current merge result to MergeResult and break the loop, go to the next merge community.
                if ((loop_free and ccf.checkLoopComm(G, Community, MergeResult_updated) == 0) or not loop_free) and ccf.checkInOutComm(G, Community, constraint, MergeResult_updated) == 0:
                    MergeResult = MergeResult_updated
                    break

            # After leaving from the for loop, we may has a successful merge or not.
            # No matter if it is merged successfully, we will choose the next community to merge in the next step
            timestep -= 1

    if len(uf.mapCommunityToNodes(MergeResult)) <= target_n:
        return MergeResult, True, {}
    else:
        return MergeResult, False, {"Time runs out"}






