import utils
import csv
import os
import CalculationFunctions as clf
import InOutFunctions as iof

samples, settings = utils.loadSettings()
txt2 = open("../results/csv_result_collection/fail.txt", "a")
for s in samples:
    G_primitive, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, _, timestep, \
    bio_flag, color_flag, height, DAG, height2, attempt_range, ub, _, _, _, _ = utils.loadData(s, settings)
    file = open(f"../results/csv_result_collection/RunTime.csv", "a", newline="")
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Benchmark", "AttemptRange", "RunTime"])
    path = f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}.txt"
    if not os.path.isfile(path):
        txt2.write(f"{s},")
        continue
    with open(path) as f:
        for line in f:
            if "Time" in line:
                line = line.split(":")[1]
                line = line.replace(" ", "")
                line = line.replace("s", "")
                line = line.replace("\n", "")
                writer.writerow([s, attempt_range, line])



    # li = [4]
    # for i in li:
    #     MergeResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{i}.txt")
    #     CellToCellEdges = clf.calculateCellEdges(G_primitive, MergeResult)
    #     print(i, TotalComm, CellToCellEdges)



