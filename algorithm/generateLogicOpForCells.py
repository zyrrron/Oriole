import findUniqueCells as uc
import InOutFunctions as iof
import UpdateFunctions as uf
import json
import csv
import utils


jsonName = 'ascon1'
samples, settings = utils.loadSettings()
for ele in range(len(samples)):

    # load settings
    s = samples[ele]
    G_primitive, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, timestep, timestep2, \
    bio_flag, color_flag, height, DAG, height2, attempt_range, ub, MaxColor, _, _, _ = utils.loadData(s, settings)

    # load partition solution and color assignment
    filename = f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint}_{attempt_range}_{MaxColor}"
    MergeResult, TotalComm = iof.loadSolution(f"{filename}.txt", s)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)
    ColorAssignment = iof.loadColorAssignment(f"{filename}_colored.txt", s)

    # load schematics / layout of the circuit
    graph_path = settings[s]['graph_path']
    JSON_file = graph_path + '/' + jsonName + '.json'
    ports, gates_info = utils.read_json(JSON_file)

    # map from signal ID to gate ID, gates here only include the primitive ones.
    mapInputSignalToGate, mapOutputSignalToGate = {}, {}
    for g in gates_info:

        # inputSignals is a dictionary: {'input': {'A': 777}, 'output': {'Y': 778}, 'type': 'NOT'}
        inputSignals = gates_info[int(g)]['input']
        for i in inputSignals:

            # A signal can be many different gates' input signal, but it can only be output by one gate
            if inputSignals[i] not in mapInputSignalToGate:
                mapInputSignalToGate[inputSignals[i]] = []
            mapInputSignalToGate[inputSignals[i]].append(str(g))

        outputSignals = gates_info[int(g)]['output']
        for i in outputSignals:
            mapOutputSignalToGate[outputSignals[i]] = str(g)

    # create 2 dictionary showing the color of input and output signals for a gate and a subgroup
    # 1. GateID: {InputSignals: [{"LastGateID": str, "Color": str}, ...], OutputSignals: [{"NextGateID": str, "Color": str}, ...]}
    # 2. CellID: {InputSignals: [{"LastCellID": str, "Edge": (LastGateID, ThisGateID), "Color": str}, ...],
    # OutputSignals: [{"NextCellID": str, "Edge": (ThisGateID, NextGateID), "Color": str}, ...]}
    # create 1 dictionary saving the internal logic gate layout of a subgroup
    # 3. CellID: {Size: int(), GateInfo: {GateID: GateType, ...}, Connections: [(Gate1 ID, Gate2 ID), ...]}
    InterGateSignalColor, CellLayout = {}, {}

    # Find input signal ID, output signal ID, their colors, and the logic layout for the current cell
    for cell in CommunityNumToNodes:
        CellLayout[cell] = {"Size": len(CommunityNumToNodes[cell]), "GateInfo": {}, "Connections": [], "Input": [], "Output": []}

        # find internal connections for the current cell
        for edge in G_primitive.edges:
            if edge[0] in CommunityNumToNodes[cell] and edge[1] in CommunityNumToNodes[cell]:
                CellLayout[cell]["Connections"].append(edge)

        # find input signal ID, output signal ID, and their colors for the current gate
        for gate in CommunityNumToNodes[cell]:

            CellLayout[cell]["GateInfo"][gate] = gates_info[int(gate)]['type']
            InterGateSignalColor[gate] = {"InputSignals": [], "OutputSignals": []}
            LastGates, NextGates, LastCells, NextCells = [], [], [], []

            # Input signal color assignment
            inputSignals = gates_info[int(gate)]['input']
            for i in inputSignals:

                EdgeInfoTemp = {}
                CellEdgeInfoTemp = {}
                if inputSignals[i] in mapOutputSignalToGate:

                    # Find input signal color info for the current gate
                    LastGate = mapOutputSignalToGate[inputSignals[i]]
                    LastGates.append(LastGate)
                    EdgeInfoTemp["LastGateID"] = LastGate
                    EdgeInfoTemp["Color"] = ColorAssignment[(LastGate, gate)]

                    # Find input signal color info for the current cell
                    if str(LastGate) in MergeResult:
                        if EdgeInfoTemp["Color"] != "gray":
                            LastCells.append(MergeResult[str(LastGate)])
                            CellEdgeInfoTemp["LastCellID"] = MergeResult[str(LastGate)]
                            CellEdgeInfoTemp["Edge"] = (LastGate, gate)
                            CellEdgeInfoTemp["Color"] = ColorAssignment[(LastGate, gate)]
                    else:
                        LastCells.append(f"Boundary Input Gate: {LastGate}")
                        CellEdgeInfoTemp["LastCellID"] = "Boundary Input Gate"
                        CellEdgeInfoTemp["Edge"] = (LastGate, gate)
                        CellEdgeInfoTemp["Color"] = "black"
                else:
                    LastGates.append("Input Signal")
                    EdgeInfoTemp["LastGateID"] = "Input Signal"
                    EdgeInfoTemp["Color"] = "black"

                    LastCells.append("Input Signal")
                    CellEdgeInfoTemp["LastCellID"] = "Input Signal"
                    CellEdgeInfoTemp["Edge"] = ("Input Signal", gate)
                    CellEdgeInfoTemp["Color"] = "black"

                InterGateSignalColor[gate]["InputSignals"].append(EdgeInfoTemp)
                if len(CellEdgeInfoTemp) > 0:
                    CellLayout[cell]["Input"].append(CellEdgeInfoTemp)

            # Output signal color assignment, one output signal can only be output by one gate. This signal only need one color.
            outputSignal = gates_info[int(gate)]['output']['Y']
            if outputSignal in mapInputSignalToGate:
                NextGates = mapInputSignalToGate[outputSignal]

                # But one signal can be the inputs of multiple gates.
                for NextGate in NextGates:
                    EdgeInfoTemp = {"NextGateID": NextGate, "Color": ColorAssignment[(gate, NextGate)]}
                    CellEdgeInfoTemp = {}

                    if str(NextGate) in MergeResult:
                        if EdgeInfoTemp["Color"] != "gray":
                            NextCells.append(MergeResult[str(NextGate)])
                            CellEdgeInfoTemp["NextCellID"] = MergeResult[str(NextGate)]
                            CellEdgeInfoTemp["Edge"] = (gate, NextGate)
                            CellEdgeInfoTemp["Color"] = ColorAssignment[(gate, NextGate)]
                    else:
                        NextCells.append(f"Boundary Output Gate: {NextGate}")
                        CellEdgeInfoTemp["NextCellID"] = "Boundary Output Gate"
                        CellEdgeInfoTemp["Edge"] = (gate, NextGate)
                        CellEdgeInfoTemp["Color"] = "black"

                    InterGateSignalColor[gate]["OutputSignals"].append(EdgeInfoTemp)
                    if len(CellEdgeInfoTemp) > 0:
                        CellLayout[cell]["Output"].append(CellEdgeInfoTemp)
            else:
                NextGates.append("Output Signal")
                EdgeInfoTemp = {"NextGateID": "Output Signal", "Color": "black"}

                NextCells.append("Output Signal")
                CellEdgeInfoTemp = {"NextCellID": "Output Signal", "Edge": (gate, "Output Signal"), "Color": "black"}

                InterGateSignalColor[gate]["OutputSignals"].append(EdgeInfoTemp)
                if len(CellEdgeInfoTemp) > 0:
                    CellLayout[cell]["Output"].append(CellEdgeInfoTemp)

    # 1. First filter: Distinguish cells by their cell and logic info and create a tree-structure dictionary to store them
    tree, leaf_count, single_leaf_count, multi_cell_nodes = uc.build_tree(CellLayout)
    print("树的叶子节点总数:", leaf_count)
    print("仅包含一个元素的叶子节点数量:", single_leaf_count)
    print("包含多个元素的叶子节点路径:", multi_cell_nodes)
    print("四层嵌套字典:", tree)

    # 2. Second filter: Distinguish cells in the same leaf by their edge info


    # Output
    csv_file = f'{out_path}/CellLayout.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Group'] + list(next(iter(CellLayout.values())).keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for group, data in CellLayout.items():
            row_data = {'Group': group}
            row_data.update(data)
            writer.writerow(row_data)

    csv_file = f'{out_path}/InterGateSignalColor.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Gate'] + list(next(iter(InterGateSignalColor.values())).keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for gate, data in InterGateSignalColor.items():
            row_data = {'Gate': gate}
            row_data.update(data)
            writer.writerow(row_data)