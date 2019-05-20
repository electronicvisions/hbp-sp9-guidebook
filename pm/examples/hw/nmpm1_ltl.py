#!/usr/bin/env python
# -*- coding: utf-8; -*-

import os
import itertools
import numpy as np

from pyhalbe import HICANN
import pyhalbe.Coordinate as C
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
marocco.default_wafer = C.Wafer(int(os.environ.get("WAFER", 33)))
runtime = Runtime(marocco.default_wafer)
pynn.setup(marocco=marocco, marocco_runtime=runtime)

#  ——— set up network ——————————————————————————————————————————————————————————

n_neurons = 10

pop = pynn.Population(n_neurons, pynn.IF_cond_exp, neuron_parameters)
pop.record()

#hicann = C.HICANNOnWafer(C.Enum(297))
#marocco.manual_placement.on_hicann(pop, hicann)

duration = 1500.0

stimulus = pynn.Population(n_neurons, pynn.SpikeSourcePoisson, {'rate' : 50})

# weights here are only dummy values
stimulus_projs = [pynn.Projection(stimulus, pop, pynn.AllToAllConnector(weights=1), target='excitatory')]
inter_projs = [pynn.Projection(pop, pop, pynn.AllToAllConnector(weights=1), target='excitatory')]

#  ——— run mapping —————————————————————————————————————————————————————————————

marocco.skip_mapping = False
marocco.backend = PyMarocco.None

pynn.reset()
pynn.run(duration)

results_synapses = runtime.results().synapse_routing.synapses()
results_placement = runtime.results().placement

#  ——— change low-level parameters before configuring hardware —————————————————

def set_sthal_params(wafer, gmax, gmax_div):
    """
    synaptic strength:
    gmax: 0 - 1023, strongest: 1023
    gmax_div: 1 - 15, strongest: 1
    """

    # for all HICANNs in use
    for hicann in wafer.getAllocatedHicannCoordinates():

        fgs = wafer[hicann].floating_gates

        # set parameters influencing the synaptic strength
        for block in C.iter_all(C.FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_gmax0, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax1, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax2, gmax)
            fgs.setShared(block, HICANN.shared_parameter.V_gmax3, gmax)

        for driver in C.iter_all(C.SynapseDriverOnHICANN):
            for row in C.iter_all(C.RowOnSynapseDriver):
                wafer[hicann].synapses[driver][row].set_gmax_div(
                    C.left, gmax_div)
                wafer[hicann].synapses[driver][row].set_gmax_div(
                    C.right, gmax_div)

        # don't change values below
        for ii in xrange(fgs.getNoProgrammingPasses()):
            cfg = fgs.getFGConfig(C.Enum(ii))
            cfg.fg_biasn = 0
            cfg.fg_bias = 0
            fgs.setFGConfig(C.Enum(ii), cfg)

        for block in C.iter_all(C.FGBlockOnHICANN):
            fgs.setShared(block, HICANN.shared_parameter.V_dllres, 275)
            fgs.setShared(block, HICANN.shared_parameter.V_ccas, 800)

# call at least once
set_sthal_params(runtime.wafer(), gmax=1023, gmax_div=1)

def find_synapses(pop_a, projections, pop_b, results_placement, results_synapses):
    """Finds synapses belonging to projections from population a to population b
    :param pop_a: population a
    :type pop_a: pynn.Population
    :param projections: list of projections
    :type projections: list of pynn.Projection
    :param pop_b: population b
    :type pop_b: pynn.Population
    :param results_placement: marocco placement result
    :type results_placement: marocco placement result
    :param results_synapses: marocco synapses result
    :type results_synapses: marocco synapses result
    :returns: synapses for projections from population a to population b
    :rtype: connection matrix with list of synapses in each element
    """

    def to_bio_neuron(nrn):
        items = results_placement.find(nrn)
        if len(items) > 1:
            raise RuntimeError("find_synapses: expected only one bio neuron")
        elif len(items) == 0:
            return None
        return items[0].bio_neuron()

    def to_hw_synapse(projection, (bna, bnb)):
        items = results_synapses.find(projection, bna, bnb)
        if len(items) > 1:
            raise RuntimeError("find_synapses: expected only one hardware synapse")
        elif len(items) == 0:
            return None
        return items[0].hardware_synapse()

    bio_nrns_a = map(to_bio_neuron, pop_a)
    bio_nrns_b = map(to_bio_neuron, pop_b)

    all_synapses = []
    
    for projection in projections:
        synapses = np.array(map(lambda (bna, bnb): to_hw_synapse(projection, (bna, bnb)), itertools.product(bio_nrns_a, bio_nrns_b)))
        synapses = synapses.reshape(pop_a.size, pop_b.size)
        all_synapses.append(synapses)

    if len(all_synapses):
        all_synapses = np.dstack(all_synapses)
        #all_synapses = np.squeeze(all_synapses, axis=2)
    else:
        all_synapses = np.array([])

    return all_synapses

def set_weight(wafer, synapse_on_wafer, weight):

    if synapse_on_wafer.shape != weight.shape:
        raise RuntimeError("set_weight synapses and weight shapes not equal: {} {}".format(synapse_on_wafer.shape, weight.shape))

    to_be_set = True
    
    for synapse, new_weight in zip(np.nditer(synapse_on_wafer[to_be_set], flags=["refs_ok", "zerosize_ok"], op_flags=["readonly"]),
                                   np.nditer(weight[to_be_set], flags=["refs_ok", "zerosize_ok"], op_flags=["readonly"])):
        if synapse.item() != None:
            print "setting {} to {}".format(synapse, new_weight)
            wafer[synapse.item().toHICANNOnWafer()].synapses[synapse.item().toSynapseOnHICANN()].weight.assign(new_weight.item())

stimulus_synapses = find_synapses(stimulus, stimulus_projs, pop, results_placement, results_synapses)
inter_synapses = find_synapses(pop, inter_projs, pop, results_placement, results_synapses)

stimulus_weights = np.load("stimulus_weights.npy")
inter_weights = np.load("inter_weights.npy")

set_weight(runtime.wafer(), stimulus_synapses, stimulus_weights)
set_weight(runtime.wafer(), inter_synapses, inter_weights)

#  ——— configure hardware ——————————————————————————————————————————————————————

marocco.skip_mapping = True
marocco.backend = PyMarocco.Hardware
# Full configuration during first step
marocco.hicann_configurator = pysthal.ParallelHICANNv4Configurator()

pynn.run(duration)
#np.savetxt("membrane.txt", pop.get_v())
np.savetxt("spikes.txt", pop.getSpikes())
pynn.reset()

# store the mapping results for visualization
runtime.results().save("results.xml.gz", True)
