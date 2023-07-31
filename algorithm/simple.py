import networkx as nx
import utils
# G = nx.read_edgelist ("../benchmark/sha256-master/src/rtl/sha256/DAG.edgelist", nodetype = str, create_using=nx.DiGraph())
# in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(G)
# G1 = utils.get_G_primitive(G, nonprimitives)
# print(G1.number_of_nodes())


def recursive_function(n):
    if n <= 0:
        return 0  # Base case: stop recursion when n is non-positive
    else:
        return 1 + recursive_function(n - 1)  # Recursive call

result = recursive_function(1000)
print(result)
