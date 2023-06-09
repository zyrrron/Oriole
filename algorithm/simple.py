import networkx as nx
G1 = nx.read_edgelist ("../benchmark/bionetwork/chris_group/jai_example/md5_opt_jai/DAG.edgelist", nodetype = str, create_using=nx.DiGraph())
G2 = nx.read_edgelist ("../benchmark/bionetwork/chris_group/jai_example/md5_opt/DAG.edgelist", nodetype = str, create_using=nx.DiGraph())
print(G1)
print(G2)
GM = nx.isomorphism.GraphMatcher(G1, G2)
print(GM.is_isomorphic())
print(GM.mapping)