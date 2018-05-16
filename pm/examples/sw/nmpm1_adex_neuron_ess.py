#!/usr/bin/env python

"""
Example Script for simulation of an AdEx neuron on the ESS

Note: Neuron and synapse parameters are chosen to be within the parameter ranges of
the default calibration.
"""

import pyhmf as pynn
#import pyNN.nest as pynn
from pymarocco import PyMarocco, Defects
import pylogging
import Coordinate as C

# configure logging
pylogging.reset()
pylogging.default_config(level=pylogging.LogLevel.INFO,
        fname="logfile.txt",
        dual=False)

# Mapping config
marocco = PyMarocco()
marocco.backend = PyMarocco.ESS # choose Executable System Specification instead of real hardware
marocco.calib_backend = PyMarocco.CalibBackend.Default
marocco.defects.backend = Defects.Backend.None
marocco.neuron_placement.skip_hicanns_without_neuron_blacklisting(False)
marocco.hicann_configurator = PyMarocco.HICANNConfigurator
marocco.experiment_time_offset = 5.e-7 # can be low for ESS, as no repeater locking required
marocco.neuron_placement.default_neuron_size(4) # default number of hardware neuron circuits per pyNN neuron
marocco.persist = "nmpm1_adex_neuron_ess.bin"
marocco.param_trafo.use_big_capacitors = False
marocco.default_wafer = C.Wafer(0)

# set-up the simulator
pynn.setup(marocco=marocco)

neuron_count = 1 # size of the Population we will create

# Set the neuron model class
neuron_model = pynn.EIF_cond_exp_isfa_ista # an Adaptive Exponential I&F Neuron

neuron_parameters = {
 'a'          : 4.0,    # adaptation variable a in nS
 'b'          : 0.0805, # adaptation variable b in pA
 'cm'         : 0.281,  # membrane capacitance nF
 'delta_T'    : 1.0,    # delta_T fom Adex mod in mV, determines the sharpness of spike initiation
 'e_rev_E'    : 0.0,    # excitatory reversal potential in mV
 'e_rev_I'    : -80.0,  # inhibitory reversal potential in mV
 'i_offset'   : 0.0,    # offset current
 'tau_m'      : 9.3667, # membrane time constant
 'tau_refrac' : 0.2,    # absolute refractory period
 'tau_syn_E'  : 20.0,   # excitatory synaptic time constant
 'tau_syn_I'  : 20.0,   # inhibitory synaptic time constant
 'tau_w'      : 144.0,  # adaptation time constant
 'v_reset'    : -70.6,  # reset potential in mV
 'v_rest'     : -70.6,  # resting potential in mV
 'v_spike'    : -40.0,  # spike detection voltage in mV
 'v_thresh'   : -50.4,  # spike initiaton threshold voltage in mV
 }

# We create a Population with 1 neuron of our neuron model
N1 = pynn.Population(size=neuron_count, cellclass=neuron_model, cellparams=neuron_parameters)

# A spike source array with spike times given in a list
spktimes = [10., 50., 65., 89., 233., 245.,255.,345.,444.4]
spike_source = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times':spktimes})

# Connect the Spike source to our neuron
pynn.Projection(spike_source, N1, pynn.OneToOneConnector(weights=0.0138445), target='excitatory')

# record the membrane voltage of all neurons of the population
N1.record_v()
# record the spikes of all neurons of the population
N1.record()

# run the simulation for 500 ms
duration = 500.
pynn.run(duration)


# After the simulation, we get Spikes
spike_times = N1.getSpikes()
for pair in spike_times:
    print "Neuron ", int(pair[0]), " spiked at ", pair[1]

# Plot voltage
do_plot = False
if do_plot:
    import pylab
    v = N1.get_v()[:,1:3] # strip ID
    pylab.plot(v[:,0], v[:,1])
    pylab.xlabel("Time [ms]")
    pylab.ylabel("Voltage [mV]")
    pylab.xlim(0,duration)
    pylab.show()

# clean up pyNN
pynn.end()
