import networkx as nx
import utils
import json
import csv
import collections
import UpdateFunctions as uf
import matplotlib.pyplot as plt
# G = nx.read_edgelist("../benchmark/sha256-master/src/rtl/sha256_core_nor/DAG.edgelist", nodetype = str, create_using=nx.DiGraph())
# print(G.number_of_nodes(), G.number_of_edges())
# in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(G)
# G1 = utils.get_G_primitive(G, nonprimitives)
# print(G1.number_of_nodes(), G1.number_of_edges())
# 打开文件并读取内容
# with open('../settings.txt', 'r') as file:
#     lines = file.readlines()
#
# # 创建一个空列表来存储第一列的值
# column1_values = []
#
# # 遍历每一行，分割并提取第一列的值
# for line in lines[68:105]:
#     columns = line.strip().split('\t')  # 如果是制表符分隔，使用'\t'，如果是空格分隔，使用' '
#     if columns:  # 确保行中有内容
#         column1_values.append(columns[0])
#
# # 输出提取的第一列值
# for value in column1_values:
#     print(value, end=",")

# pos = nx.spring_layout(G, seed=42)
# nx.draw_networkx(G, with_labels=True)
# plt.title("Directed Acyclic Graph (DAG)")
# plt.show()

# nx.draw_networkx(G, with_labels=True)
# Display the plot
# plt.show()

# MergeResultList = [{"1": "1", "2": "2", "3": "3", "4": "4", "5": "5"},
#                    {"1": "1", "2": "2", "3": "3", "4": "4", "5": "4"},
#                    {"1": "1", "2": "2", "3": "3", "4": "4", "5": "3"},
#                    {"1": "1", "2": "2", "3": "2", "4": "4", "5": "4"}]
# d = {}
# out_path = "../results/test/simple"
# for i in range(len(MergeResultList)):
#
#     # calculate the number of cells for each merge result now
#     ll = len(collections.Counter(list(MergeResultList[i].values())))
#     d[i] = ll

# Sort the given dictionary, tmp is a dictionary with key = index in MergeResult, value = length of that merge result
# print(f"{len(d)} possible solutions to be checked for edge coloring assignment!")
# tmp = sorted(d.items(), key=lambda x: (x[1], x[0]), reverse=False)
# tmp = dict(tmp)
#
# # save it to a csv file
# new_d = []
#
# with open(f"{out_path}/merge_result_list.csv", "w", newline="") as csv_file:
#     fieldnames = ["Total Number of Comms", "Solution"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#
#     for i in tmp:
#         ComSol = uf.mapCommunityToNodes(MergeResultList[i])
#         new_d.append([len(ComSol), MergeResultList[i]])
#         info_row = {"Total Number of Comms": len(ComSol), "Solution": ComSol}
#         writer.writerow(info_row)
#
# # save the sorted merge result list to a json file
#
# with open(f"{out_path}/merge_result_list.json", "w") as json_file:
#     json.dump(new_d, json_file)


# # load json file
# out_path = "../results/sha256/sha256_8"
# # with open(f"{out_path}/merge_result_list.json", "r") as json_file:
#     # loaded_data = json.load(json_file)
#
# json_file = open(f"{out_path}/merge_result_list_8_4_[1, 500].json", "r")
# json_data = json_file.read()
# json_file.close()
# loaded_data = json.loads(json_data)
# samples, settings = utils.loadSettings()
#
# # Assign colors to each cell-cell edge iteratively
# for s in samples:
#
#     G, S_bounds, _, _, constraint, loop_free, priority, out_path, _, _, bio_flag, _, _, _, _, _ = utils.loadData(s, settings)
#     MergeResultList = json.loads(json_data)
#     for i in range(len(MergeResultList)):
#         SolLength, MergeResult = MergeResultList[i]
#         CellToCellEdges = []
#         for u, v in G.edges:
#             if u in MergeResult and v in MergeResult:
#                 ComU, ComV = MergeResult[u], MergeResult[v]
#                 if ComU != ComV:
#                     CellToCellEdges.append((u, v))
#         EdgeIndexInfo_file = open(f"{out_path}/CellEdgesInfo.csv", "a", newline="")
#         writer = csv.writer(EdgeIndexInfo_file)
#         writer.writerow([i, len(CellToCellEdges)])


