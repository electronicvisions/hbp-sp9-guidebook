#!/usr/bin/env python
# -*- coding: utf-8; -*-

import argparse
import numpy as np

import elephant.spike_train_generation as stgen
import quantities as Q

parser = argparse.ArgumentParser()
parser.add_argument('simulator',
                    type=str,
                    choices=['bss', 'nest'],
                    help='Simulation backend to use')
args = parser.parse_args()

if args.simulator == 'bss':
    import os
    import pyhmf as pynn

    from pyhalco_hicann_v2 import Wafer, HICANNOnWafer
    from pyhalco_common import Enum
    from pysthal.command_line_util import init_logger
    from pymarocco import PyMarocco

    init_logger("WARN", [
    ("guidebook", "DEBUG"),
    ("marocco", "TRACE"),
    ("Calibtic", "DEBUG"),
    ("sthal", "INFO")
    ])

    marocco = PyMarocco()
    wafer_int = int(os.environ.get("WAFER", 33))
    marocco.default_wafer = Wafer(wafer_int)

    marocco.calib_path = "/wang/data/commissioning/BSS-1/rackplace/{}/calibration/current".format(wafer_int)
    marocco.calib_backend = PyMarocco.CalibBackend.XML
    marocco.defects.path = "/wang/data/commissioning/BSS-1/rackplace/{}/derived_plus_calib_blacklisting/current".format(wafer_int)
    marocco.backend = PyMarocco.Hardware

    pynn.setup(marocco=marocco)
else:
    import pyNN.nest as pynn
    pynn.setup(timestep=0.1)

neuron_parameters = {
    'cm': 0.2,     # nF
    'v_reset': -20, # mV
    'v_rest': -50,  # mV
    'v_thresh': 100,# mV
    'e_rev_I': -80, # mV
    'e_rev_E': 20,  # mV
    'tau_m': 5,    # ms
    'tau_syn_E': 2, # ms
    'tau_syn_I': 2, # ms
}

#  ——— set up network ——————————————————————————————————————————————————————————

pop = pynn.Population(1, pynn.IF_cond_exp, neuron_parameters)

pop.record()
pop.record_v()

if args.simulator == 'bss':
    hicann = HICANNOnWafer(Enum(297))
    marocco.manual_placement.on_hicann(pop, hicann)

connector = pynn.AllToAllConnector(weights=0.01)

exc_spike_times = [
    250,
    500,
    520,
    540,
    1250,
]

inh_spike_times = [
    750,
    1000,
    1020,
    1040,
    1250,
]

duration = 3000.0

np.random.seed(5321)
exc_spike_times = np.concatenate([
    stgen.homogeneous_poisson_process(20 * Q.Hz, 250 * Q.ms, 750 * Q.ms, as_array=True),
    stgen.homogeneous_poisson_process(20 * Q.Hz, 1750 * Q.ms, 2750 * Q.ms, as_array=True),
])

inh_spike_times = np.concatenate([
    stgen.homogeneous_poisson_process(20 * Q.Hz, 1000 * Q.ms, 1500 * Q.ms, as_array=True),
    stgen.homogeneous_poisson_process(20 * Q.Hz, 1750 * Q.ms, 2750 * Q.ms, as_array=True),
])


stimulus_exc = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times' : exc_spike_times})
stimulus_inh = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times' : inh_spike_times})

projections = [
    pynn.Projection(stimulus_exc, pop, connector, target='excitatory'),
    pynn.Projection(stimulus_inh, pop, connector, target='inhibitory'),
]

#  ——— run  —————————————————————————————————————————————————————————————

pynn.run(duration)

np.savetxt("membrane_{}.txt".format(args.simulator), pop.get_v())
np.savetxt("spikes_{}.txt".format(args.simulator), pop.getSpikes())
