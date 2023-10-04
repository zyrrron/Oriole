import utils
import CalculationFunctions as clf
import InOutFunctions as iof

samples, settings = utils.loadSettings()
for s in samples:
    G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, _, out_path, _, timestep, \
    bio_flag, height, DAG, height2, attempt_range, ub = utils.loadData(s, settings)
    li = [4]
    for i in li:
        MergeResult, TotalComm = iof.loadSolution(f"{out_path}/sol_after_merge_{S_bounds[1]}_{constraint[0]}_{attempt_range}_{i}.txt")
        CellToCellEdges = clf.calculateCellEdges(G_primitive, MergeResult)
        print(i, TotalComm, CellToCellEdges)



