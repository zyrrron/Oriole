import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import InOutFunctions as iof
import CommunityFunctions as ccf
import copy
import UpdateFunctions as uf


# propaganda checking stop after the given depth
def prepareNeighborOrder(G, CenterCommunity, CurrentResult, constraint, bio_flag, height, S_bound, ub, path_set):

    # Initiate the values we will return
    CurrentResult_new = copy.deepcopy(CurrentResult)

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
def enlargeCommunity(G, Community, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, CurrentResult, bio_flag, height):

    # Return to the last level if it arrives to the size constraints, time constraint or current community meets all constraints
    if ccf.checkSize(CurrentResult, Community) > S_bounds[1]:
        return CurrentResult, False, {Community}, timestep
    if timestep < 0:
        return CurrentResult, False, {"Time runs out"}, timestep

    # When the current community meets all constraints, transfer to the next one
    if ((loop_free and ccf.checkLoopComm(G, Community, CurrentResult, bio_flag) == 0) or not loop_free) and ccf.checkInOutComm(G, Community, constraint, CurrentResult, bio_flag) == 0:

        # Find other pending communities
        PendingCommunities = ccf.findPendingCommunities(G, CurrentResult, constraint, bio_flag)

        # If no other pending communities, return current result.
        if len(PendingCommunities) == 0:
            return CurrentResult, True, {}, timestep

        # If there are still some pending communities, find the worst one and solve it next.
        Community = ccf.findWorstCommunity(G, PendingCommunities, CurrentResult, bio_flag)
        print("PendingCommunities: ", PendingCommunities)
        print("Community: ", Community)

        # Start solving the new pending community
        CurrentResult, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, Community, S_bounds, ConstraintType,
                                                                               constraint, loop_free, priority, timestep-1, CurrentResult, bio_flag, height)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the last level and try the other neighbor nodes
        if VerifyFlag:
            return CurrentResult, True, {}, timestep
        else:
            return CurrentResult, False, {Community}, timestep

    rewards_new, CurrentResult_new, path_set = prepareNeighborOrder(G, Community, CurrentResult, constraint, bio_flag, height, S_bounds, 2, {})

    # start the middle part of backtracking
    for c in rewards_new:
        if timestep % 100000 == 0:
            print("Rewards: ", c, rewards_new[c])
            print("Timestep: ", timestep)

        # Update the current verify result after adding the neighbor community
        # Here we create a new variable C_updated, because we can use C_new as the original data in the 3rd stage of backtracking
        CurrentResult_updated = ccf.addNeighborComm(CurrentResult_new, c, Community)
        CurrentResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, Community, S_bounds, ConstraintType,
                                                                         constraint, loop_free, priority, timestep-1,  CurrentResult_updated, bio_flag, height)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the scenario before adding the current neighbor node
        if VerifyFlag:
            return CurrentResult_updated, True, {}, timestep
        elif timestep < 0:
            return CurrentResult_new, False, {"Time runs out"}, timestep

    return CurrentResult_new, VerifyFlag, ErrorLog, timestep


# Merging Method 1: Enlarge Communities in the Merge stage using two level neighbor propaganda checking. (every time merge one or two communities)
def enlargeCommunityMerge(G, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, Result, target_n, bio_flag, height):
    MergeResult = copy.deepcopy(Result)

    # There are 2 possible conditions to return back
    # 1. meet target n constraint
    # 2. meet time constraint
    totalNum = 0
    count = 1

    while timestep >= 0 and len(uf.mapCommunityToNodes(MergeResult)) > target_n:
        path_set = set()
        CommunityNumToNodes1 = uf.mapCommunityToNodes(MergeResult)
        if totalNum == len(uf.mapCommunityToNodes(MergeResult)):
            count += 1
        else:
            count = 1
            totalNum = len(uf.mapCommunityToNodes(MergeResult))
        if count == 2: break
        print(f"Current number of communities: {len(uf.mapCommunityToNodes(MergeResult))}, stay in this number for {count} times")

        # Find all possible to-be-merged communities and sort them with rewards. Scan them in this order.
        MergeCommunities = ccf.findMergeCommunities(G, MergeResult, constraint, bio_flag)

        # Try to merge the communities in the order of MergeCommunities
        for Community in MergeCommunities:

            # Find all neighbor communities around the chosen community.
            # And get the sorted rewards dictionary for all the neighbor communities
            rewards_sorted, _, path_set = prepareNeighborOrder(G, Community, MergeResult, constraint, bio_flag, height, S_bounds, 3, path_set)

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
                    MergeResult = MergeResult_updated
                    break

            # After leaving from the for loop, we may have a successful merge or not.
            # Keep checking until all communities are checked.
            CommunityNumToNodes2 = uf.mapCommunityToNodes(MergeResult)
            timestep -= 1

    if len(uf.mapCommunityToNodes(MergeResult)) <= target_n:
        return MergeResult, True, {}
    else:
        return MergeResult, False, {"Time runs out"}

