import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import CommunityFunctions as ccf
import copy


# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving the highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, PendingCommunity, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, CurrentVerifyResult):

    # Return to the last level if it arrives to the size constraints or current community meets all constraints
    if ccf.checkSize(CurrentVerifyResult, PendingCommunity) > S_bounds[1]:
        return CurrentVerifyResult, False, {PendingCommunity}, timestep
    if ccf.checkLoopComm(G, PendingCommunity, CurrentVerifyResult) == 0 and ccf.checkInOutComm(G, PendingCommunity, constraint, CurrentVerifyResult) == 0:
        return CurrentVerifyResult, True, {}, timestep
    if timestep < 0:
        return CurrentVerifyResult, False, {"Time runs out"}, timestep

    # Initiate the values we will return
    CurrentVerifyResult_new = copy.deepcopy(CurrentVerifyResult)
    VerifyFlag = True
    ErrorLog = {}

    # calculate the rewards provided by all neighbor communities
    NeighborComm = ccf.findAllNeighborsComm(G, PendingCommunity, CurrentVerifyResult)
    rewards = {}
    for c in NeighborComm:
        rewards[c] = calf.calculateRewardComm(G, c, PendingCommunity, CurrentVerifyResult, constraint)

    # find the community provides the highest reward, sort this rewards dictionary first and try them in the order
    tmp = sorted(rewards.items(), key=lambda x: x[1], reverse=True)
    rewards_new = dict(tmp)

    # start the middle part of backtracking
    for c in rewards_new:
        print("Rewards: ", rewards_new[c])
        print("Timestep: ", timestep)

        # Prepare for the backtracking
        c_old_community = CurrentVerifyResult_new[c]

        # update the current verify result after adding the neighbor community
        CurrentVerifyResult_updated = ccf.addNeighborComm(CurrentVerifyResult_new, c, PendingCommunity)
        CurrentVerifyResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, PendingCommunity, S_bounds, ConstraintType,
                                                                         constraint, loop_free, priority, timestep-1,
                                                                         CurrentVerifyResult_updated)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we try the next neighbor community and change the CurrentVerifyResult back
        if VerifyFlag:

            # Find other pending communities
            PendingCommunities = ccf.findPendingCommunities(G_primitive, CurrentVerifyResult_updated, constraint)

            # If no other pending communities, save current result and return.
            if len(PendingCommunities) == 0:
                iof.writeVerifySolution(out_path, G_primitive, CurrentVerifyResult_updated)
                return CurrentVerifyResult_updated, True, {}, timestep
            print("PendingCommunities: ", PendingCommunities)

            # If there are still some pending communities, find the worst one and solve it next.
            PendingCommunity = ccf.findWorstCommunity(G_primitive, PendingCommunities, CurrentVerifyResult)
            print("PendingCommunity: ", PendingCommunity)

            # Use the updated new current verify result and the new worst community
            CurrentVerifyResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, PendingCommunity, S_bounds,
                                                                             ConstraintType,
                                                                             constraint, loop_free, priority, timestep-1,
                                                                             CurrentVerifyResult_updated)
        else:


    return CurrentVerifyResult_new, VerifyFlag, ErrorLog, timestep
