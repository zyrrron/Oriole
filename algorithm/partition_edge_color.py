from merging import Merging
from verification import Verification
from EdgeColoring import EdgeColoring
import time
import utils

samples, settings = utils.loadSettings()
begintime =  time.time()
for ele in range(len(samples)):

    # load settings
    s = samples[ele]
    G_primitive, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, timestep, timestep2, \
    bio_flag, color_flag, height, DAG, height2, attempt_range, ub, MaxColor, trace_back, check_interval, SingleFlag = utils.loadData(s, settings)

    # Verification, Merge and Edge Coloring
    Verification(G_primitive, S_bounds, ConstraintType, constraint, loop_free, out_path, timestep, bio_flag, height, ub)
    Merging(G_primitive, S_bounds, target_n, constraint, loop_free, out_path, timestep2, bio_flag, color_flag, height, height2, attempt_range.copy(), ub,s)
    EdgeColoring(G_primitive, S_bounds, constraint, out_path, bio_flag, DAG, attempt_range, MaxColor, trace_back, check_interval, SingleFlag, s)
