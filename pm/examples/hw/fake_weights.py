#!/usr/bin/env python

import numpy as np

np.save("stimulus_weights.npy", np.full((10,10,1), 7, dtype=int))
np.save("inter_weights.npy", np.full((10,10,1), 5, dtype=int))
