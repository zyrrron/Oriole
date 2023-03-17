import os
import UpdateFunctions as uf

# Write current verify solution into a output file
def writeVerifySolution(out_path, G, CurrentVerifyResult):
    outfile = out_path + '/sol_after_verify.txt'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f_out = open(outfile, 'w')
    if len(CurrentVerifyResult) == 0:
        f_out.write(f'Community 0: {list(G.nodes)}')
    else:
        NewCommunityNumToNodes, CurrentVerifyResult = uf.updateCommunityNum(CurrentVerifyResult)
        for key in NewCommunityNumToNodes:
            f_out.write(f'Community {key}: {NewCommunityNumToNodes[key]}\n')


# If no solution find, return current best clustering solution, and the return the community caused the problem.
def reportIssue(out_path, G_primitive, VerifyResult, ErrorLog):
    pass


# Save current verification solution and send it to "merging.py"
def saveSolution():
    pass