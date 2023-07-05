# -*- coding: utf-8 -*-
# @Time    : 27/03/2023 00:40
# @Author  : Marshall
# @FileName: json_util.py
import json
import numpy as np

class NumpyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        else:
            return super(NumpyJsonEncoder, self).default(o)