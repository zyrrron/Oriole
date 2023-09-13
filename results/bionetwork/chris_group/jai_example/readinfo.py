import os
import shutil
import utils
import networkx as nx
import csv


def print_subfolder_names():
    current_directory = os.getcwd()
    dictD = {}
    attempt_range = [1,5]
    edgeNum = [4, 5, 6]
    cell = 8

    for root, directories, files in os.walk(current_directory):
        if root != current_directory and os.path.dirname(root) == current_directory:
            directories = sorted(directories, key=lambda x: (len(x), x))
            rootName = root.split('/')[-1]
            dictD[rootName] = list()

            # check results in md5 benchmarks
            if rootName in ["md5_opt_ExceptXORXNOR","md5_opt_all","md5_opt_nand","md5_opt_nor2","md5_opt_ExceptXORXNOR_12","md5_opt_all_12",
                            "md5_opt_nand_12","md5_opt_nor2_12","md5_opt_ExceptXORXNOR_20","md5_opt_all_20","md5_opt_nand_20","md5_opt_nor2_20"]:

                # get partition solution info in this benchmark
                for edge in edgeNum:
                    info = f"_{cell}_{edge}"
                    G = nx.read_edgelist(f"{rootName}/sol_after_merge{info}.txt", nodetype=str, create_using=nx.DiGraph())
                    nodeOld, edgeOld = G.number_of_nodes(), G.number_of_edges()
                    in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(G)
                    G1 = utils.get_G_primitive(G, nonprimitives)
                    nodeNew, edgeNew = G1.number_of_nodes(), G1.number_of_edges()

                    # non-primitive nodes will also be checked
                    l = f"{rootName}\t../benchmark/electronic-circuits/{rootName}\t./lib\tTRUE\t1,7\t3\tlow\t2,2\t4\tTRUE\tC\t0\t./results/{rootName}"
                    dictD[rootName].append([rootName, l, rootName, nodeOld, edgeOld, nodeNew, edgeNew])

    dictD = dict(sorted(dictD.items()))
    txt0 = open("fileNames.txt", "a")
    txt1 = open("settingNames.txt", "a")
    graphInfo = open(f"graphInfo.csv", "a", newline="")
    writer = csv.writer(graphInfo)
    if graphInfo.tell() == 0:
        writer.writerow(["benchmark", "node", "edge", "PrimitiveNode", "PrimitiveEdge"])

    for d in dictD:
        for val in dictD[d]:
            txt0.write(f"{val[0]},")
            txt1.write(f"{val[1]}\n")
            writer.writerow(val[2:])


print_subfolder_names()
