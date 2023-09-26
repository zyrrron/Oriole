import os
import UpdateFunctions as uf
import networkx as nx


def writeSolution(out_path, filename, G, CurrentResult, CostTime):
    outfile = out_path + filename
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')
    if len(CurrentResult) == 0:
        print(f"Current number of communities is 1!")
        f_out.write(f"Time Cost: {CostTime}s\n")
        f_out.write(f'Community 1: {list(G.nodes)}')
    else:
        NewCommunityNumToNodes, CurrentResult = uf.updateCommunityNum(CurrentResult)
        f_out.write(f"Time Cost: {CostTime}s\n")
        # Print and save the current solution
        # print(NewCommunityNumToNodes)
        for key in NewCommunityNumToNodes:
            f_out.write(f'Community {key}: {NewCommunityNumToNodes[key]}\n')


# Write edge list with color
def writeColoredEdgeList(out_path, filename, G):
    outfile = out_path + filename
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    nx.write_edgelist(G,outfile,data=["color"])


# If no solution find, return the community caused the problem.
def reportIssue(out_path, ErrorLog, info=""):
    outfile = out_path + f'/error_report{info}.txt'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')

    f_out.write(f"Error caused by: {ErrorLog}. Please check constraints and the edges connected to this node.")
    print("Verification failed!")
    print("Error caused by: ", ErrorLog)


# 1. Save current verification solution and send it to "merging.py"
# 2. Save current merge solution and send it to "EdgeColoring.py"
def loadSolution(path, s):

    # read data from verification result
    with open(path) as f:
        next(f)
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

    # 1. change it to the same format in verification stage CurrentResult
    # 2. change it to the same format in merge stage CurrentResult
    VerifyResult = {}
    CommunityNum = 1
    for ele in d:
        for e in ele:
            VerifyResult[e] = str(CommunityNum)
        CommunityNum += 1
    return VerifyResult


# If current number of communities in the merge solution is bigger than target N, report issue
def reportMergeIssue(G_primitive, out_path, solutionfile, MergeResult, ErrorLog, attempt_range, VerifyResult, target_n, CostTime, str=""):
    outfile = out_path + f'/error_report{str}.txt'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')
    CommunityNumToNodesAfterMerge = uf.mapCommunityToNodes(MergeResult)
    CommunityNumToNodesBeforeMerge = uf.mapCommunityToNodes(VerifyResult)

    if len(CommunityNumToNodesAfterMerge) == 0:
        print("No solution can satisfy our edge coloring assignment!")
        return

    f_out.write(f"Target N is: {target_n}. Stop caused by: {ErrorLog}. \n")
    f_out.write(f"During {attempt_range} attempts of different merging strategy, we decrease the number of communities ")
    f_out.write(f"from {len(CommunityNumToNodesBeforeMerge)} to {len(CommunityNumToNodesAfterMerge)}\n")
    f_out.write(f"Time Cost: {CostTime}s\n")
    print(f"Target N is: {target_n}. Stop caused by: {ErrorLog}.")
    print(f"Current number of communities is decreased from {len(CommunityNumToNodesBeforeMerge)} to {len(CommunityNumToNodesAfterMerge)}!")

    # Print and save the current solution
    writeSolution(out_path, solutionfile, G_primitive, MergeResult, CostTime)
