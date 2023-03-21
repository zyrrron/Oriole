import utils
import networkx as nx
import matplotlib.pyplot as plt

samples, settings = utils.loadSettings()
for s in samples:
    G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep = utils.loadData(s, settings)
    nx.draw_spring(G_primitive, with_labels=True)
    plt.savefig(f"{out_path}/{s}_fig_spring.jpg")
    plt.clf()
