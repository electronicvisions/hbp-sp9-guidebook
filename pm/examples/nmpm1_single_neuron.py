# -*- coding: utf-8 -*-
#
# Minimal Working Example of a single neuron and a single spike source on NMPM1
#
# Andreas Stöckel, October 2015
#
# Modified by S. Schmitt, October 2015
# Modified by S. Schmitt, July 2016

import numpy as np
import pylogging
import pyhmf as pynn
from pymarocco import PyMarocco
from pyhalbe.Coordinate import Wafer, HICANNOnWafer, Enum

# Number of hardware neurons used for a logical neuron
neuron_size = 4

# Excitatory neuron weight
w_exc = 0.1

# IF_cond_exp parameters
params = {
    'v_reset': -70,
    'v_rest': -50,
    'v_thresh': -45,
    'e_rev_I': -70,
    'e_rev_E': 10,
    'tau_m': 16,
    'tau_syn_E': 17,
    'tau_syn_I': 17,
}

# Deactivate logging -- not doing so causes multi-megabyte logfiles which fail
# to be transfered back to the Neuromorphic Compute Platform, causing the job
# to indefenitely hang in the "running" state
for domain in ["Default", "marocco", "sthal.HICANNConfigurator.Time", "hicann-system", "halbe"]:
    pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.ERROR)

# but we need a little bit of output to know what's going on
pylogging.set_loglevel(pylogging.get("Calibtic"), pylogging.LogLevel.DEBUG)
pylogging.set_loglevel(pylogging.get("marocco"), pylogging.LogLevel.DEBUG)

# Setup the router/placement engine
marocco = PyMarocco()
marocco.neuron_placement.default_neuron_size(neuron_size)

# for backend Hardware
# temporary method to allow locking of synapse drivers by using
# the background generators also for FPGA input routes
marocco.neuron_placement.restrict_rightmost_neuron_blocks(True)

marocco.neuron_placement.minimize_number_of_sending_repeaters(False)
marocco.backend = PyMarocco.Hardware
marocco.calib_backend = PyMarocco.XML
marocco.calib_path = "/wang/data/calibration/review_2016"
marocco.persist = "results.bin"
marocco.hicann_configurator = PyMarocco.HICANNv4Configurator

marocco.default_wafer = Wafer(33)

# choose membrane capacitance
# marocco.param_trafo.use_big_capacitors = False

use=HICANNOnWafer(Enum(367)) # choose hicann
marocco.analog_enum = 0
marocco.hicann_enum = use.id().value()

#output
#marocco.membrane = "membrane.dat" # voltage trace
marocco.wafer_cfg = "wafer.bin"   # configuration
marocco.roqt = "example.roqt"     # visualization

#example for blacklisting, one pyredman.Hicann instance per HICANN
#h = pyredman.Hicann()
#h.drivers().disable(SynapseDriverOnHICANN(C.right, C.Y(4)))
#h.neurons().disable(NeuronOnHICANN(Enum(0)))
#marocco.defects.inject(use, h)

# Setup the NMPM1 PyNN interface "pyhmf"
pynn.setup(marocco = marocco)

# Create the spike source -- generate a spike all 100ms for 10s
spike_times = range(0, 10000, 100)
in_0 = pynn.Population(5, pynn.SpikeSourceArray, {
    'spike_times': spike_times
})

# Create the target neuron
nn_0 = pynn.Population(1, pynn.IF_cond_exp, params)

# Introduce the neuron to the placement engine
marocco.manual_placement.on_hicann(nn_0, use)

# Add a connection between the spike source in_0 and the neuron nn_0 -- the
# connection needs to be added neuron_size times
for _ in xrange(neuron_size):
    pynn.Projection(in_0, nn_0,
        pynn.FromListConnector([(0, 0, w_exc, 0.0)]), target = 'excitatory')

# Run the simulation, continue running for 1s after the last spike
pynn.run(max(spike_times) + 1000.0)

# End the simulation, gather results
pynn.end()

# Fetch the spike times and print them
spikes = nn_0.getSpikes()
print ">>>>", spikes
np.savetxt("spikes.dat", spikes)
