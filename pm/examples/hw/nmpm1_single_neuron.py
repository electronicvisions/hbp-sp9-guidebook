#!/usr/bin/env python
# -*- coding: utf-8; -*-

import numpy as np

from pyhalbe import HICANN
import pyhalbe.Coordinate as C
from pysthal.command_line_util import init_logger

import pyhmf as pynn
from pymarocco import PyMarocco, Defects
from pymarocco.runtime import Runtime
from pymarocco.coordinates import LogicalNeuron
from pymarocco.results import Marocco

init_logger("WARN", [
    ("guidebook", "DEBUG"),
    ("marocco", "DEBUG"),
    ("calibtic", "DEBUG"),
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
marocco.neuron_placement.default_neuron_size(4)
marocco.neuron_placement.minimize_number_of_sending_repeaters(False)
marocco.merger_routing.strategy(marocco.merger_routing.one_to_one)

marocco.bkg_gen_isi = 125
marocco.pll_freq = 125e6

marocco.backend = PyMarocco.Hardware
marocco.calib_backend = PyMarocco.XML
marocco.defects.path = marocco.calib_path = "/wang/data/calibration/ITL_2016"
marocco.defects.backend = Defects.XML
marocco.default_wafer = C.Wafer(33)
marocco.param_trafo.use_big_capacitors = True
marocco.input_placement.consider_firing_rate(True)
marocco.input_placement.bandwidth_utilization(0.8)

runtime = Runtime(marocco.default_wafer)
pynn.setup(marocco=marocco, marocco_runtime=runtime)

#  ——— set up network ——————————————————————————————————————————————————————————

pop = pynn.Population(1, pynn.IF_cond_exp, neuron_parameters)

pop.record()
pop.record_v()

hicann = C.HICANNOnWafer(C.Enum(367))
marocco.manual_placement.on_hicann(pop, hicann)

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

marocco.skip_mapping = False
marocco.backend = PyMarocco.None

pynn.reset()
pynn.run(duration)

#  ——— change low-level parameters before configuring hardware —————————————————

def set_sthal_params(wafer, gmax, gmax_div):
    for hicann in wafer.getAllocatedHicannCoordinates():
        fgs = wafer[hicann].floating_gates
        for ii in xrange(fgs.getNoProgrammingPasses()):
            cfg = fgs.getFGConfig(C.Enum(ii))
            cfg.fg_biasn = 0
            cfg.fg_bias = 0
            fgs.setFGConfig(C.Enum(ii), cfg)

        for block in C.iter_all(C.FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_gmax0, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax1, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax2, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax3, gmax)

        for block in C.iter_all(C.FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_dllres, 275)
            fgs.setShared(block, HICANN.shared_parameter.V_ccas, 800)

        for driver in C.iter_all(C.SynapseDriverOnHICANN):
            for row in C.iter_all(C.RowOnSynapseDriver):
                wafer[hicann].synapses[driver][row].set_gmax_div(
                    C.left, gmax_div)
                wafer[hicann].synapses[driver][row].set_gmax_div(
                    C.right, gmax_div)

set_sthal_params(runtime.wafer(), gmax=1023, gmax_div=1)

#  ——— configure hardware ——————————————————————————————————————————————————————

marocco.skip_mapping = True
marocco.backend = PyMarocco.Hardware
# Full configuration during first step
marocco.hicann_configurator = PyMarocco.HICANNv4Configurator

for digital_weight in [5, 10, 15]:
    logger.info("running measurement with digital weight {}".format(digital_weight))
    for proj in projections:
        proj_item, = runtime.results().synapse_routing.synapses().find(proj)
        synapse = proj_item.hardware_synapse()

        proxy = runtime.wafer()[synapse.toHICANNOnWafer()].synapses[synapse]
        proxy.weight = HICANN.SynapseWeight(digital_weight)

    pynn.run(duration)
    np.savetxt("membrane_w{}.txt".format(digital_weight), pop.get_v())
    np.savetxt("spikes_w{}.txt".format(digital_weight), pop.getSpikes())
    pynn.reset()

    # only change digital parameters from now on
    marocco.hicann_configurator = PyMarocco.NoResetNoFGConfigurator
