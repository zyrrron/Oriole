import os
import shutil
import utils
import networkx as nx
import csv


def print_subfolder_names():
    current_directory = os.getcwd()
    dictD = {}

    for root, directories, files in os.walk(current_directory):
        if root != current_directory and os.path.dirname(root) == current_directory:
            directories = sorted(directories, key=lambda x: (len(x), x))
            rootName = root.split('/')[-1]
            dictD[rootName] = list()
            if rootName in ['4', '5', '6', '7', '8']:
                for folder_name in directories:
                    # get node and edge info in this benchmark
                    G = nx.read_edgelist(f"{rootName}/{folder_name}/DAG.edgelist", nodetype=str, create_using=nx.DiGraph())
                    nodeOld, edgeOld = G.number_of_nodes(), G.number_of_edges()
                    in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(G)
                    G1 = utils.get_G_primitive(G, nonprimitives)
                    nodeNew, edgeNew = G1.number_of_nodes(), G1.number_of_edges()

                    # primitive_only benchmarks
                    l = f"{rootName}input_{folder_name}\t../benchmark/input-boolean-circuits/{rootName}/{folder_name}\t./lib\tTRUE\t1,7\t3\tlow\t2,2\t4\tTRUE\tC\t0\t./results/input-boolean-circuits/{rootName}/{folder_name}"
                    dictD[rootName].append([f"{rootName}input_{folder_name}", l, f"{rootName}input_{folder_name}", nodeOld, edgeOld, nodeNew, edgeNew])

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


def delete_matching_subfolders(input_folder_name):
    current_directory = os.getcwd()

    for root, directories, files in os.walk(current_directory):
        if root != current_directory:
            for directory in directories:
                if directory == input_folder_name:
                    folder_path = os.path.join(root, directory)
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder: {folder_path}")


# Example usage:
# delete_matching_subfolders("nparts")
print_subfolder_names()
