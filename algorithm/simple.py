import networkx as nx
import utils
import matplotlib.pyplot as plt
G = nx.read_edgelist("../benchmark/test/test4/DAG.edgelist", nodetype = str, create_using=nx.DiGraph())
# in_nodes, out_nodes, nonprimitives = utils.get_nonprimitive_nodes(G)
# G1 = utils.get_G_primitive(G, nonprimitives)
# print(G1.number_of_nodes())


nx.draw_networkx(G, with_labels=True)
# Display the plot
plt.show()


