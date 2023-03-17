import InitiateFunctions as inf
import CalculationFunctions as calf
import NodeFunctions as nf
import CommunityFunctions as ccf

# Try to enlarge the given community i.
# After searching and calculating all the gains for moving each neighbor node into community i,
# move the node j giving the highest positive gain to our community i.
# If all gains are negative or the node number achieve the size constraint, stop enlarge.
# Check if current community i meets all constraints every time when we move node j into community i.
# Record it if meets all constraints.
# Better use recursion here.
def enlargeCommunity(G, PendingCommunity, S_bounds, ConstraintType, constraint, loop_free, priority, timestep, CurrentVerifyResult, size):
    # calculate the rewards provided by all neighbor communities
    NeighborComm = ccf.findAllNeighborsComm(G, PendingCommunity, CurrentVerifyResult)
    rewards = {}
    for c in NeighborComm:
        rewards[c] = calf.calculateRewardComm(G, c, PendingCommunity, CurrentVerifyResult, constraint)

    # find the community provides the highest reward, sort this rewards dictionary first and try them in the order
    tmp = sorted(rewards.items(), key=lambda x: x[1], reverse=True)
    rewards_new = dict(tmp)
    print(rewards_new)
    return
