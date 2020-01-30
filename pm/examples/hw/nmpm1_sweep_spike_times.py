#!/usr/bin/env python
# -*- coding: utf-8; -*-

import os
import numpy as np

from pyhalbe import HICANN
from pyhalco_hicann_v2 import Wafer, HICANNOnWafer, SynapseDriverOnHICANN
from pyhalco_hicann_v2 import RowOnSynapseDriver, FGBlockOnHICANN
from pyhalco_common import Enum, iter_all
from pysthal.command_line_util import init_logger
import pysthal

import pyhmf as pynn
from pymarocco import PyMarocco, Defects
from pymarocco.runtime import Runtime
from pymarocco.coordinates import LogicalNeuron
from pymarocco.results import Marocco

init_logger("WARN", [
    ("guidebook", "DEBUG"),
    ("marocco", "DEBUG"),
    ("Calibtic", "DEBUG"),
    ("sthal", "INFO")
])

import pylogging
logger = pylogging.get("guidebook")

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

marocco = PyMarocco()
marocco.default_wafer = Wafer(int(os.environ.get("WAFER", 33)))
runtime = Runtime(marocco.default_wafer)
pynn.setup(marocco=marocco, marocco_runtime=runtime)

#  ——— set up network ——————————————————————————————————————————————————————————

pop = pynn.Population(1, pynn.IF_cond_exp, neuron_parameters)

pop.record()
pop.record_v()

hicann = HICANNOnWafer(Enum(297))
marocco.manual_placement.on_hicann(pop, hicann)

connector = pynn.AllToAllConnector(weights=1)

duration = 1500.0

# initialize without spike times
stimulus_exc = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times': []})
stimulus_neuron = stimulus_exc[0]

projections = [
    pynn.Projection(stimulus_exc, pop, connector, target='excitatory'),
]

#  ——— run mapping —————————————————————————————————————————————————————————————

marocco.skip_mapping = False
marocco.backend = PyMarocco.None

pynn.reset()
pynn.run(duration)

#  ——— change low-level parameters before configuring hardware —————————————————

def set_sthal_params(wafer, gmax, gmax_div):
    """
    synaptic strength:
    gmax: 0 - 1023, strongest: 1023
    gmax_div: 2 - 30, strongest: 2
    """

    # for all HICANNs in use
    for hicann in wafer.getAllocatedHicannCoordinates():

        fgs = wafer[hicann].floating_gates

        # set parameters influencing the synaptic strength
        for block in iter_all(FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_gmax0, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax1, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax2, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax3, gmax)

        for driver in iter_all(SynapseDriverOnHICANN):
            for row in iter_all(RowOnSynapseDriver):
                wafer[hicann].synapses[driver][row].set_gmax_div(HICANN.GmaxDiv(gmax_div))

        # don't change values below
        for ii in xrange(fgs.getNoProgrammingPasses()):
            cfg = fgs.getFGConfig(Enum(ii))
            cfg.fg_biasn = 0
            cfg.fg_bias = 0
            fgs.setFGConfig(Enum(ii), cfg)

        for block in iter_all(FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_dllres, 275)
            fgs.setShared(block, HICANN.shared_parameter.V_ccas, 800)

# call at least once
set_sthal_params(runtime.wafer(), gmax=1023, gmax_div=2)

#  ——— configure hardware ——————————————————————————————————————————————————————

for proj in projections:
    proj_items = runtime.results().synapse_routing.synapses().find(proj)
    for proj_item in proj_items:
        synapse = proj_item.hardware_synapse()
        proxy = runtime.wafer()[synapse.toHICANNOnWafer()].synapses[synapse]
        proxy.weight = HICANN.SynapseWeight(15)

marocco.skip_mapping = True
marocco.backend = PyMarocco.Hardware

for n, spike_times in enumerate([[100,110], [200,210], [300,310]]):

    runtime.results().spike_times.set(stimulus_neuron, spike_times)

    pynn.run(duration)
    np.savetxt("membrane_n{}.txt".format(n), pop.get_v())
    np.savetxt("spikes_n{}.txt".format(n), pop.getSpikes())
    pynn.reset()

    # skip checks
    marocco.verification = PyMarocco.Skip
    marocco.checkl1locking = PyMarocco.SkipCheck

# store the last result for visualization
runtime.results().save("results.xml.gz", True)
