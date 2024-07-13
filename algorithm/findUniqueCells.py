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

# find unique groups in the CellLayout
D = {
    'cell0': {'Size': 3, 'GateInfo': {'1': 'NOR', '2': 'NOR', '0': 'NOR'}},
    'cell9': {'Size': 1, 'GateInfo': {'3': 'NOT'}},
    'cell8': {'Size': 3, 'GateInfo': {'4': 'NOR', '5': 'NOT', "6": 'NOT'}},
    'cell7': {'Size': 2, 'GateInfo': {'7': 'NOT', '8': 'NOT'}},
    'cell5': {'Size': 2, 'GateInfo': {'9': 'NOR', '10': 'NOT'}},
    'cell4': {'Size': 3, 'GateInfo': {'12': 'NOR', '13': 'NOT', "14": 'NOR'}},
    'cell11': {'Size': 3, 'GateInfo': {'15': 'NOT', '16': 'NOT', "17": 'NOR'}},
    'cell12': {'Size': 3, 'GateInfo': {'18': 'NOR', '19': 'NOR', "20": 'NOR'}},
}

def get_gate_info_stats(gate_info):
    gate_types = len(set(gate_info.values()))
    not_count = list(gate_info.values()).count('NOT')
    nor_count = list(gate_info.values()).count('NOR')
    return gate_types, not_count, nor_count


def build_tree(D):
    tree = {}
    leaf_count = 0
    single_leaf_count = 0
    multi_cell_nodes = []

    for key, value in D.items():
        size = value['Size']
        gate_types, not_count, nor_count = get_gate_info_stats(value['GateInfo'])

        if size not in tree:
            tree[size] = {}
        if gate_types not in tree[size]:
            tree[size][gate_types] = {}
        if not_count not in tree[size][gate_types]:
            tree[size][gate_types][not_count] = {}
        if nor_count not in tree[size][gate_types][not_count]:
            tree[size][gate_types][not_count][nor_count] = []

        tree[size][gate_types][not_count][nor_count].append(key)

    for size in tree:
        for gate_types in tree[size]:
            for not_count in tree[size][gate_types]:
                for nor_count in tree[size][gate_types][not_count]:
                    leaf = tree[size][gate_types][not_count][nor_count]
                    leaf_count += 1
                    if len(leaf) == 1:
                        single_leaf_count += 1
                    else:
                        multi_cell_nodes.append([size, gate_types, not_count, nor_count])

    return tree, leaf_count, single_leaf_count, multi_cell_nodes


def splitByInput()

