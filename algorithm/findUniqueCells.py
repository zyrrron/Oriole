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


# Get basic gate info
def get_gate_info(gate_info):
    gate_types = len(set(gate_info.values()))
    not_count = list(gate_info.values()).count('NOT')
    nor_count = list(gate_info.values()).count('NOR')
    return gate_types, not_count, nor_count


# Get the total number of Input / Output signals, colors being used for Input / Output, specific color for each Input / Output edge.
def get_io_info(value):
    Input, Output = value['Input'], value['Output']
    InputNum = len(Input)
    OutputNum = len(Output)
    InputColor = set()
    OutputColor = set()
    ColorDomain = {'Input': [], 'Output': []}

    # Find colors for each Input / Output edge,
    for InputSignal in Input:
        ColorDomain['Input'].append(InputSignal['Color'])
        InputColor.add(InputSignal['Color'])

    for OutputSignal in Output:
        ColorDomain['Output'].append(OutputSignal['Color'])
        OutputColor.add(OutputSignal['Color'])

    return InputNum, OutputNum, len(InputColor), len(OutputColor), ColorDomain


# Create a dictionary that users can find the input/output edges according to a given gate.
def GateToEdges(CellInfo):
    GateToInputEdges, GateToOutputEdges = {}, {}
    Edges = {}
    edge_index = 0
    CommunicationEdges = {'InputEdge': [], 'OutputEdge': []}

    # Re-name the edges inside the cell
    for edge in CellInfo['Connections']:
        Edges[f"S{edge_index}"] = {'Edge': edge, 'Color': 'gray'}

        # Append this edge index to the output edge list of its start gate
        if edge[0] in GateToOutputEdges:
            GateToOutputEdges[edge[0]].append(f"S{edge_index}")
        else:
            GateToOutputEdges[edge[0]] = [f"S{edge_index}"]

        # Append this edge index to the input edge list of its end gate
        if edge[1] in GateToInputEdges:
            GateToInputEdges[edge[1]].append(f"S{edge_index}")
        else:
            GateToInputEdges[edge[1]] = [f"S{edge_index}"]
        edge_index += 1

    # Re-name the intercellular Input / Output signals
    edge_index = 0
    for info in CellInfo['Input']:
        Edges[f"Input{edge_index}"] = {'Edge': info['Edge'], 'Color': info['Color']}
        CommunicationEdges['InputEdge'].append(f"Input{edge_index}")

        # Append this edge index to the input edge list of its end gate
        if info['Edge'][1] in GateToInputEdges:
            GateToInputEdges[info['Edge'][1]].append(f"Input{edge_index}")
        else:
            GateToInputEdges[info['Edge'][1]] = [f"Input{edge_index}"]
        edge_index += 1

    edge_index = 0
    for info in CellInfo['Output']:
        Edges[f"Output{edge_index}"] = {'Edge': info['Edge'], 'Color': info['Color']}
        CommunicationEdges['OutputEdge'].append(f"Output{edge_index}")

        # Append this edge index to the output edge list of its end gate
        if info['Edge'][0] in GateToOutputEdges:
            GateToOutputEdges[info['Edge'][0]].append(f"Output{edge_index}")
        else:
            GateToOutputEdges[info['Edge'][0]] = [f"Output{edge_index}"]
        edge_index += 1

    return GateToInputEdges, GateToOutputEdges, Edges, CommunicationEdges


# Create logic expression set for the current cell
def createLogic(CellInfo, CommunicationEdges, ColorDomain, GateToInputEdges, GateToOutputEdges, Edges):
    LogicExpressions = {}

    # For each output gate, we have multiple steps to creat the logic expression set.
    # Step 0 (before while loop): Add each output signal index Output_X from CommunicationEdges['OutputEdge'] to a queue. (First In First Out)
    # Step 1 (while loop starts): If the queue is not empty, use the fist signal index in the queue to find the detail edge info in Edges.
    #   If it is in CommunicationEdges['InputEdge'], remove the signal and go to the next while loop.
    # Step 2: Find the corresponding gate and its logic type. Determine the number of input edges (1 or 2) (Now we only detect NOT and NOR)
    # Step 3: Find the corresponding input edge(s) in GateToInputEdges, append the source input edges into queue, add a new expression to the
    # logic expression set, [Current Signal Index, NOR, Input Edge 1, Input Edge 2] / [Current Signal Index, NOT, Input Edge 1]
    # Step 4: Go to the next loop
    for CurrentOutEdge in CommunicationEdges['OutputEdge']:
        queue = [CurrentOutEdge]
        while queue:
            if queue[0] in CommunicationEdges['OutputEdge']:
                queue.remove(0)
    return LogicExpressions


def createFeatureTable(D):
    FeatureTable = {}
    for key, value in D.items():
        CurrentCellFeature = {}

        # Initiate basic info for the feature table.
        # Assign index for the gates communicating with other cells and get color info for such gates.
        CurrentCellFeature['Size'] = value['Size']
        CurrentCellFeature['TypeNum'], CurrentCellFeature['NotNum'], CurrentCellFeature['NorNum'] = get_gate_info(value['GateInfo'])
        CurrentCellFeature['InputNum'], CurrentCellFeature['OutputNum'], CurrentCellFeature['InputColorNum'], \
            CurrentCellFeature['OutputColorNum'], ColorDomain = get_io_info(value)
        CurrentCellFeature['ColorDomain'] = ColorDomain

        # Create a dictionary that can map gate to input/output edges through edge index, each edge has its identical index.
        GateToInputEdges, GateToOutputEdges, Edges, CommunicationEdges = GateToEdges(value)

        # Create logic expression function for each cell
        CurrentCellFeature['LogicExpression'] = createLogic(value, CommunicationEdges, ColorDomain, GateToInputEdges, GateToOutputEdges, Edges)

        # Add this current cell feature to the feature table.
        FeatureTable[key] = CurrentCellFeature
    return FeatureTable

