# Copyright (C) 2023 by
# Yangruirui Zhou <yrrzhou@bu.edu>, CIDAR Lab, Boston University
# All rights reserved.
# OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.
# Start working on the verification stage

import uc_createFeatureTable as ucft
import InOutFunctions as iof
import UpdateFunctions as uf
import json
import csv
import utils

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

#
def distinguishCells(CellInfo):
    pass