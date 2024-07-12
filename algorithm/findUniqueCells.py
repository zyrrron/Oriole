import argparse
import sys
import copy
import InOutFunctions as iof
import UpdateFunctions as uf
import json
import csv
import utils
import EdgeFunctions as ef
from collections import defaultdict
import collections
import time


def build_tree(d, depth=1):
    if depth == 1:
        key = 'Size'
        value_func = lambda x: x
    elif depth == 2:
        key = 'GateInfo'
        value_func = lambda gateinfo: len(set(gateinfo.values()))
    elif depth == 3:
        key = 'GateInfo'
        value_func = lambda gateinfo: sum(1 for gate in gateinfo.values() if gate == 'NOT')
    elif depth == 4:
        key = 'GateInfo'
        value_func = lambda gateinfo: sum(1 for gate in gateinfo.values() if gate == 'NOR')
    else:
        return d  # Leaf node

    tree = {}
    for cell_name, attributes in d.items():
        value = value_func(attributes[key]) if key == 'GateInfo' else attributes[key]

        if value not in tree:
            tree[value] = []

        tree[value].append(cell_name)

    for value, subnodes in tree.items():
        if depth < 4:
            subtree = build_tree({k: d[k] for k in subnodes}, depth + 1)
            if isinstance(subtree, list):
                tree[value] = subtree
            else:
                tree[value] = [subtree]

    return tree


def count_leaf_nodes(tree, path=[], multi_cell_nodes=[]):
    if isinstance(tree, dict):
        leaf_count = 0
        single_leaf_count = 0
        for key, subtree in tree.items():
            count, single_count, multi_nodes = count_leaf_nodes(subtree, path + [key], multi_cell_nodes)
            leaf_count += count
            single_leaf_count += single_count
            multi_cell_nodes.extend(multi_nodes)
        return leaf_count, single_leaf_count, multi_cell_nodes
    elif isinstance(tree, list):
        if len(tree) > 1:
            multi_cell_nodes.append(path)
        return len(tree), 1 if len(tree) == 1 else 0, multi_cell_nodes


# find unique groups in the CellLayout
D = {
    'cell0': {'Size': 3, 'GateInfo': {'1': 'NOR', '2': 'NOR', '0': 'NOR'}},
    'cell9': {'Size': 1, 'GateInfo': {'3': 'NOT'}},
    'cell8': {'Size': 3, 'GateInfo': {'4': 'NOR', '5': 'NOT', "6": 'NOT'}},
    'cell7': {'Size': 2, 'GateInfo': {'7': 'NOT', '8': 'NOT'}},
    'cell5': {'Size': 2, 'GateInfo': {'9': 'NOR', '10': 'NOT'}},
    'cell6': {'Size': 1, 'GateInfo': {'11': 'NOR'}},
    'cell1': {'Size': 2, 'GateInfo': {'19': 'NOT', '20': 'NOR'}},
    'cell2': {'Size': 2, 'GateInfo': {'15': 'NOR', '16': 'NOR'}},
    'cell3': {'Size': 2, 'GateInfo': {'17': 'NOR', '18': 'NOT'}},
    'cell4': {'Size': 3, 'GateInfo': {'12': 'NOR', '13': 'NOT', "14": 'NOR'}},
    'cell11': {'Size': 3, 'GateInfo': {'15': 'NOT', '16': 'NOT', "17": 'NOR'}},
    'cell12': {'Size': 3, 'GateInfo': {'18': 'NOR', '19': 'NOR', "20": 'NOR'}},
}


tree = build_tree(D)

# 计算叶子节点和包含多个元素的叶子节点路径
leaf_count, single_leaf_count, multi_cell_nodes = count_leaf_nodes(tree)

import pprint
print("树结构:")
pprint.pprint(tree)
print("\n总叶子节点数:", leaf_count)
print("仅含一个元素的叶子节点数:", single_leaf_count)
print("包含多个元素的叶子节点路径:")
for path in multi_cell_nodes:
    print(path)

