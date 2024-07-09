import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import networkx as nx
import utils
import copy
import UpdateFunctions as uf
import InOutFunctions as iof

# Load samples and settings
samples, settings = utils.loadSettings()
for s_index in range(len(samples)):

    # Load merge result
    s = samples[s_index]
    G, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, _, _, bio_flag, _, _, DAG, _, attempt_range, \
    _, ColorNum, _, _, _ = utils.loadData(s, settings)
    MergeResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{ColorNum}.txt", s)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)

    # Load edge list with color
    ResultColored = {}
    with open(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{ColorNum}_colored.txt") as f:
        for line in f:
            parts = line.strip().split(" ")
            key = tuple(parts[:2])
            value = parts[2]
            ResultColored[key] = value

    # Set optional colors for nodes
    colors = [plt.cm.jet(i / TotalComm) for i in range(TotalComm)]
    colorNode = copy.deepcopy(CommunityNumToNodes)
    i = 0
    for k in colorNode:
        colorNode[k] = colors[i]
        i += 1
    node_colors = []
    for node in DAG.nodes():
        if node not in MergeResult:
            node_colors.append("gray")
        else:
            node_colors.append(colorNode[MergeResult[node]])

    # Set optional colors for edges
    colors = ["red", "orange", "yellow", "blue", "green", "purple", "pink", "cyan"]
    edge_colors = []
    for edge in DAG.edges():
        if ResultColored[edge] not in ["black", "gray"]:
            ColorIndex = int(ResultColored[edge][-1])
            edge_colors.append(colors[ColorIndex])
        else:
            edge_colors.append(ResultColored[edge])

    # Two layouts to show the graph clearly
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    pos1 = nx.kamada_kawai_layout(DAG)
    pos2 = nx.circular_layout(DAG)

    # Kamada-Kawai Layout
    plt.subplot(1, 2, 1)
    nx.draw_networkx(DAG, pos1, ax=ax1, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    ax1.set_title("Kamada-Kawai Layout")

    # Circular Layout
    plt.subplot(1, 2, 2)
    nx.draw_networkx(DAG, pos2, ax=ax2, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    ax2.set_title("Circular Layout")

    plt.suptitle(f'Partitioned by {TotalComm} subgroups using {ColorNum} colors with {attempt_range[1]} attempts', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{out_path}/graph_detail_{attempt_range}.png')
    plt.show()

