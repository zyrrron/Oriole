import os
import UpdateFunctions as uf


def writeSolution(out_path, filename, G, CurrentResult):
    outfile = out_path + filename
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')
    if len(CurrentResult) == 0:
        f_out.write(f'Community 1: {list(G.nodes)}')
    else:
        NewCommunityNumToNodes, CurrentResult = uf.updateCommunityNum(CurrentResult)

        # Print and save the current solution
        print(NewCommunityNumToNodes)
        for key in NewCommunityNumToNodes:
            f_out.write(f'Community {key}: {NewCommunityNumToNodes[key]}\n')


# If no solution find, return the community caused the problem.
def reportIssue(out_path, ErrorLog):
    outfile = out_path + '/error_report.txt'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')

    f_out.write(f"Error caused by: {ErrorLog}. Please check constraints and the edges connected to this node.")
    print("Verification failed!")
    print("Error caused by: ", ErrorLog)


# Save current verification solution and send it to "merging.py"
def loadVerifySolution(path, s):

    # read data from verification result
    with open(f"{path}/sol_after_verify.txt") as f:
        i = 0
        d = []
        for line in f:
            i += 1
            line = line.replace('\'','')
            line = line.split('[')[1]
            line = line.split(']')[0]
            line = line.replace(' ', '')
            line = line.split(',')
            d.append(line)

    # change it to the same format in verification stage CurrentResult
    VerifyResult = {}
    CommunityNum = 1
    for ele in d:
        for e in ele:
            VerifyResult[e] = str(CommunityNum)
        CommunityNum += 1
    return VerifyResult

# If current number of communities in the merge solution is bigger than target N, report issue
def reportMergeIssue(out_path, MergeResult, ErrorLog, timestep, VerifyResult):
    outfile = out_path + '/error_report.txt'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')
    CommunityNumToNodesAfterMerge = uf.mapCommunityToNodes(MergeResult)
    CommunityNumToNodesBeforeMerge = uf.mapCommunityToNodes(VerifyResult)

    f_out.write(f"Error caused by: {ErrorLog}. \n")
    f_out.write(f"After {timestep} steps merge attempts, we decrease the number of communities from {len(CommunityNumToNodesBeforeMerge)} to ")
    f_out.write(f"{len(CommunityNumToNodesAfterMerge)}")
    print("Merge failed in the current target N!")
    print("Error caused by: ", ErrorLog)
    print(f"Current number of communities is decreased from {len(CommunityNumToNodesBeforeMerge)} to {len(CommunityNumToNodesAfterMerge)}!")