#!/usr/bin/env python
# -*- coding: utf-8; -*-

import os
import numpy as np
import pyhmf as pynn
from pymarocco import PyMarocco
from pymarocco.runtime import Runtime
from pymarocco.results import Marocco
import Coordinate as C
import pysthal
from pysthal.command_line_util import init_logger

init_logger("WARN", [
    ("guidebook", "DEBUG"),
    ("marocco", "DEBUG"),
    ("Calibtic", "DEBUG"),
    ("sthal", "INFO")
])

marocco = PyMarocco()
runtime = Runtime(C.Wafer(int(os.environ.get("WAFER", 22))))
pynn.setup(marocco=marocco, marocco_runtime=runtime)

#  ——— set up network ——————————————————————————————————————————————————————————

neuron_parameters = {
    'cm': 0.2,
    'v_reset': -70.,
    'v_rest': -20.,
    'v_thresh': -10,
    'e_rev_I': -100.,
    'e_rev_E': 60.,
    'tau_m': 20.,
    'tau_refrac': 0.1,
    'tau_syn_E': 5.,
    'tau_syn_I': 5.,
}

pop = pynn.Population(10, pynn.IF_cond_exp, neuron_parameters)
pop.record()

hicann = C.HICANNOnWafer(C.Enum(297))
marocco.manual_placement.on_hicann(pop, hicann)

# force a very high weight
connector = pynn.AllToAllConnector(weights=1)

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

duration = 1500.0

stimulus_exc = pynn.Population(1, pynn.SpikeSourceArray, {
    'spike_times': exc_spike_times})
stimulus_inh = pynn.Population(1, pynn.SpikeSourceArray, {
    'spike_times': inh_spike_times})

projections = [
    pynn.Projection(stimulus_exc, pop, connector, target='excitatory'),
    pynn.Projection(stimulus_inh, pop, connector, target='inhibitory'),
]

#  ——— run mapping —————————————————————————————————————————————————————————————

# fill results
marocco.skip_mapping = False
marocco.backend = PyMarocco.None
pynn.run(0)

marocco.skip_mapping = True
marocco.backend = PyMarocco.Hardware
marocco.verification = PyMarocco.Skip

for n, neuron in enumerate(pop):

    item = runtime.results().placement.find(neuron)[0]
    logical_neuron = item.logical_neuron()
    runtime.results().analog_outputs.record(logical_neuron)

    pynn.run(duration)

    np.savetxt("membrane_n{}.txt".format(n), pop.get_v())
    np.savetxt("spikes_n{}.txt".format(n), pop.getSpikes())

    pynn.reset()
    runtime.results().analog_outputs.unrecord(logical_neuron)
