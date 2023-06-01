'''
--------------------------------------------------------------------------------
Description:
Roadmap:
Written by W.R. Jackson <wrjackso@bu.edu>, DAMP Lab 2020
--------------------------------------------------------------------------------
'''

import cobra
import matplotlib.pyplot as plt
import networkx as nx
import tqdm
# graph = nx.DiGraph()
# input_model = cobra.io.read_sbml_model("e_coli_core.xml")
# for reaction_object in input_model.reactions:
#     name = reaction_object.id
#     metabolites = reaction_object.metabolites
#     reactants = reaction_object.reactants
#     products = reaction_object.products
#     for reactant in reactants:
#         for product in products:
#             graph.add_edge(reactant, product)


### save to edgelist 
# f_out = open('DAG.edgelist', 'w')
# for edge in list(graph.edges()):
#     f_out.write(str(edge[0]) + ' ' + str(edge[1]) + ' ' + '{'+'}' + '\n')


pos = nx.kamada_kawai_layout(graph)
plt.figure(num=None, figsize=(8,8), dpi=80)
nx.draw(
    graph,
    pos=pos,
    horizontalalignment='left',
    verticalalignment='bottom',
    node_color='coral'
)
plt.savefig('./core/DAG.pdf')
plt.show()
print(f'The Number of Nodes is {len(graph.nodes)}')
print(f'The Number of Edges is {len(graph.edges)}')