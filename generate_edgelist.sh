
#	Copyright (C) 2021 by
#	Jing Zhang <jgzhang@bu.edu>, Densmore Lab, Boston University
# 	All rights reserved.
#	OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.

# Map raw reads

#python3 $BIN_PATH/generate_edgelist.py -settings ./settings.txt -samples gray,gray4,gray8,gray16,gray64,mux4,mux8,mux16,mux32,mux64,parity,parity4,parity8,parity16,parity32,parity64,priority_encoder4,priority_encoder16,priority_encoder32,voter2,voter4,voter8,voter16,voter32
#python3 $BIN_PATH/generate_edgelist.py -settings ./settings.txt -samples md5_opt
python3 generateEdgeList.py -settings ./settings.txt -samples case3_h
