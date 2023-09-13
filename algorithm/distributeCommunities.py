import utils
import InOutFunctions as iof
import UpdateFunctions as uf
import collections
import os
import csv
import CommunityFunctions as ccf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def countEdgesForEachCell():

    # Load samples and settings
    samples, settings = utils.loadSettings()
    csvpath = "../results/bionetwork/chris_group/jai_example"
    SoltionNum = {}
    maxedges = [6,5,4]

    # Check samples iteratively
    for s in samples:

        # Load merge result
        G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep, timestep2, bio_flag, height, DAG, \
        height2, attempt_range, ub = utils.loadData(s, settings)
        maxsize = S_bounds[1]
        ResultList = [s]
        for maxedge in maxedges:
            info = f"_{maxsize}_{maxedge}_{attempt_range}"
            if os.path.exists(f"{out_path}/sol_after_merge{info}.txt"):
                MergeResult = iof.loadSolution(f"{out_path}/sol_after_merge{info}.txt", s)
            else:
                continue
            CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
            ResultList.append(len(CommunityNumToNodes))

            NumOfSize = collections.defaultdict(int)
            NumOfCommunications = collections.defaultdict(int)

            # record the distribution of cell-cell communication numbers and cell size
            for c in CommunityNumToNodes:
                l = len(CommunityNumToNodes[c])
                NumOfSize[l] += 1
                NumInEdegs = ccf.findIncomingEdgesComm(G_primitive, c, MergeResult, bio_flag)
                NumOutEdegs = ccf.findOutgoingEdgesComm(G_primitive, c, MergeResult, bio_flag)
                NumOfCommunications[len(NumInEdegs)+len(NumOutEdegs)] += 1
                # print(c, l, CommunityNumToNodes[c], NumInEdegs, NumOutEdegs)

            # print()
            # print("Shows the distribution of cells by their total number of gates:")
            # print(NumOfSize)
            #
            # print()
            # print("Shows the distribution of cells by their total number of cell-cell communications excluding input / output:")
            # print(NumOfCommunications)

            # plot the NumOfSize, x-axis is the size of that cell, y-axis is the number of this size exists in the final partition result
            x_labels = list(NumOfSize.keys())
            y_values = list(NumOfSize.values())

            plt.bar(x_labels, y_values)
            plt.title(f"Distribution for Max size: {maxsize}, Max Intercellular Edge: {maxedge}")
            plt.xlabel("# of gates")
            plt.ylabel("Count")
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

            for x, y in zip(x_labels, y_values):
                plt.text(x, y, str(y), ha='center', va='bottom')
            plt.savefig(f"{out_path}/distribution_chart{info}.png")
            # plt.show()

        SoltionNum[s] = ResultList
    graphInfo = open(f"{csvpath}/SolutionInfo.csv", "w", newline="")
    writer = csv.writer(graphInfo)
    FirstLine = ["benchmark"]
    for i in maxedges:
        FirstLine.append(f"intercellular edges <= {i}")
    if graphInfo.tell() == 0:
        writer.writerow(FirstLine)

    for d in SoltionNum:
        writer.writerow(SoltionNum[d])


countEdgesForEachCell()
