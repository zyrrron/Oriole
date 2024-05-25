import argparse
import sys
import copy
import InOutFunctions as iof
import UpdateFunctions as uf
import json
import csv
import utils
import EdgeFunctions as ef
import collections
import time
sys.path.append("../Oriole")


jsonName = 'sha256_core_nor'
MaxColor = [8]
samples, settings = utils.loadSettings()
for ele in range(len(samples)):
    s = samples[ele]
    G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep, timestep2, \
    bio_flag, height, DAG, height2, attempt_range, ub = utils.loadData(s, settings)
    MergeResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{MaxColor[ele]}.txt", s)
    CommunityNumToNodes = uf.mapCommunityToNodes(MergeResult)

    graph_path = settings[s]['graph_path']
    JSON_file = graph_path + '/' + jsonName + '.json'
    ports, gates_info = utils.read_json(JSON_file)

    # map back from signal to gate
    mapInputSignalToGate, mapOutputSignalToGate = {}, {}
    for g in gates_info:
        inputSignals = gates_info[int(g)]['input']
        for i in inputSignals:
            mapInputSignalToGate[inputSignals[i]] = g
        outputSignals = gates_info[int(g)]['output']
        for i in outputSignals:
            mapOutputSignalToGate[outputSignals[i]] = g

    # create logic operation dictionary for each community
    NewDict = {}
    for key in CommunityNumToNodes:
        size = len(CommunityNumToNodes[key])
        l, ll = [], []

        # find input signals and output signals for the current gate
        for gate in CommunityNumToNodes[key]:
            LastGates, NextGates, LastCell, NextCell = [], [], [], []
            inputSignals = gates_info[int(gate)]['input']
            for i in inputSignals:
                if inputSignals[i] in mapOutputSignalToGate:
                    LastGate = mapOutputSignalToGate[inputSignals[i]]
                    LastGates.append(LastGate)
                    if str(LastGate) in MergeResult:
                        LastCell = MergeResult[str(LastGate)]
                    else:
                        LastCell = f"Non-primitive Input Gate: {LastGate}"
                else:
                    LastGates.append("Input Signal")
                    LastCell = "Input Signal"

            outputSignals = gates_info[int(gate)]['output']
            for i in outputSignals:
                if outputSignals[i] in mapInputSignalToGate:
                    NextGate = mapInputSignalToGate[outputSignals[i]]
                    NextGates.append(NextGate)
                    if str(NextGate) in MergeResult:
                        NextCell = MergeResult[str(NextGate)]
                    else:
                        NextCell = f"Non-primitive Input Gate: {NextGate}"
                else:
                    NextGates.append("Output Signal")
                    NextCell = "Output Signal"

            temp = {"Gate": gate, "Type": gates_info[int(gate)]['type'], "LastCell": LastCell, "NextCell": NextCell}
            temp2 = {"Gate": gate, "LastGate": LastGates, "NextGate": NextGates}
            l.append(temp)
            ll.append(temp2)
        NewDict[key] = {"Size": size, "Gates": CommunityNumToNodes[key], "Intercellular Info": l, "Gate Info": ll}

        # find the source community sending input signals to the current community
        # for inputSignal in CellInputs:
        #     if inputSignal in mapOutputSignalToGate:
        #         LastGate = mapOutputSignalToGate[inputSignal]
        #         if str(LastGate) in MergeResult:
        #             LastCell = MergeResult[str(LastGate)]
        #         else:
        #             LastCell = f"Input gate: {LastGate}"
        #     else:
        #         LastCell = "Outside the circuit"
        #     LastCells.add(LastCell)

        # find the next community receiving the output signals from the current community
        # for outputSignal in CellOutputs:
        #     if outputSignal in mapInputSignalToGate:
        #         NextGate = mapInputSignalToGate[outputSignal]
        #         if str(NextGate) in MergeResult:
        #             NextCell = MergeResult[str(NextGate)]
        #         else:
        #             NextCell = f"Output gate: {NextGate}"
        #     else:
        #         NextCell = "Outside the circuit"
        #     NextCells.add(NextCell)

        # print(key, CommunityNumToNodes[key], CellInputs, CellOutputs, LastCells, NextCells)
        # d = {"GateType": GateType, "LastCells": LastCells, "NextCells": NextCells,
        #      "InputSignalsForThisCell": CellInputs, "OutputSignalsForThisCell": CellOutputs}
        # NewDict[key] = d

    csv_file = f'{out_path}/detailed_info.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Group'] + list(next(iter(NewDict.values())).keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for group, data in NewDict.items():
            row_data = {'Group': group}
            row_data.update(data)
            writer.writerow(row_data)



