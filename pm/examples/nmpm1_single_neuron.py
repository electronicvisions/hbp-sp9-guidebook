# -*- coding: utf-8 -*-

#
# Minimal Working Example of a single neuron and a single spike source on NMPM1
#
# Andreas Stöckel, October 2015
#

import pylogging
import pyhmf as pynn
from pymarocco import PyMarocco
from pyhalbe.Coordinate import HICANNGlobal, Enum

# Number of hardware neurons used for a logical neuron
neuron_size = 4

# Excitatory neuron weight
w_exc = 0.004 

# IF_cond_exp parameters
params = {
    'cm': 0.2,
    'v_reset': -70,
    'v_rest': -50,
    'v_thresh': -47,
    'e_rev_I': -60,
    'e_rev_E': -40,
    'tau_refrac': 20,
    'tau_m': 409,
}

# Deactivate logging -- not doing so causes multi-megabyte logfiles which fail
# to be transfered back to the Neuromorphic Compute Platform, causing the job
# to indefenitely hang in the "running" state
for domain in ["Default", "marocco", "sthal.HICANNConfigurator.Time"]:
    pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.ERROR)

# Setup the router/placement engine
marocco = PyMarocco()
marocco.placement.setDefaultNeuronSize(neuron_size)
marocco.placement.use_output_buffer7_for_dnc_input_and_bg_hack = True
marocco.placement.minSPL1 = False
marocco.backend = PyMarocco.Hardware
marocco.calib_backend = PyMarocco.XML
marocco.calib_path = "/wang/data/calibration/wafer_0"

# Setup the NMPM1 PyNN interface "pyhmf"
pynn.setup(marocco = marocco)

# Create the spike source -- generate a spike all 100ms for 10s
spike_times = range(0, 10000, 100)
in_0 = pynn.Population(1, pynn.SpikeSourceArray, {
    'spike_times': spike_times
})

# Create the target neuron
nn_0 = pynn.Population(1, pynn.IF_cond_exp, params)

# Introduce the neuron to the placement engine
marocco.placement.add(nn_0, HICANNGlobal(Enum(276)))

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
