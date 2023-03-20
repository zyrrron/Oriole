import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import InOutFunctions as iof
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

    # Return to the last level if it arrives to the size constraints, time constraint or current community meets all constraints
    if ccf.checkSize(CurrentVerifyResult, PendingCommunity) > S_bounds[1]:
        return CurrentVerifyResult, False, {PendingCommunity}, timestep
    if timestep < 0:
        return CurrentVerifyResult, False, {"Time runs out"}, timestep

    # When the current community meets all constraints, transfer to the next one
    if ccf.checkLoopComm(G, PendingCommunity, CurrentVerifyResult) == 0 and ccf.checkInOutComm(G, PendingCommunity, constraint, CurrentVerifyResult) == 0:

        # Find other pending communities
        PendingCommunities = ccf.findPendingCommunities(G, CurrentVerifyResult, constraint)

        # If no other pending communities, return current result.
        if len(PendingCommunities) == 0:
            return CurrentVerifyResult, True, {}, timestep

        # If there are still some pending communities, find the worst one and solve it next.
        PendingCommunity = ccf.findWorstCommunity(G, PendingCommunities, CurrentVerifyResult)
        print("PendingCommunities: ", PendingCommunities)
        print("PendingCommunity: ", PendingCommunity)

        # Start solving the new pending community
        CurrentVerifyResult, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, PendingCommunity, S_bounds, ConstraintType,
                                                                               constraint, loop_free, priority, timestep-1,
                                                                               CurrentVerifyResult)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the last level and try the other neighbor nodes
        if VerifyFlag:
            return CurrentVerifyResult, True, {}, timestep
        else:
            return CurrentVerifyResult, False, {PendingCommunity}, timestep


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
        if timestep % 100 == 0:
            print("Rewards: ", c, rewards_new[c])
            print("Timestep: ", timestep)

        # Update the current verify result after adding the neighbor community
        # Here we create a new variable C_updated, because we can use C_new as the original data in the 3rd stage of backtracking
        CurrentVerifyResult_updated = ccf.addNeighborComm(CurrentVerifyResult_new, c, PendingCommunity)
        CurrentVerifyResult_updated, VerifyFlag, ErrorLog, timestep = enlargeCommunity(G, PendingCommunity, S_bounds, ConstraintType,
                                                                         constraint, loop_free, priority, timestep-1,
                                                                         CurrentVerifyResult_updated)

        # If the current pending community is solved, then we choose the next one to deal with
        # If not, we backtrack to the scenario before adding the current neighbor node
        if VerifyFlag:
            return CurrentVerifyResult_updated, True, {}, timestep
        elif timestep < 0:
            return CurrentVerifyResult_new, False, {"Time runs out"}, timestep

    return CurrentVerifyResult_new, VerifyFlag, ErrorLog, timestep
