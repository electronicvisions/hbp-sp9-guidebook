"""


"""

# --- Import external libraries ----------------

import pyNN.nest as sim
import numpy.random
import matplotlib.pyplot as plt


# --- Parameters -------------------------------

n_populations = 11
population_size = 8
neuron_parameters = {
    'cm': 0.2,
    'v_reset': -70,
    'v_rest': -70,
    'v_thresh': -47,
    'e_rev_I': -70,
    'e_rev_E': 0.0,
}
weight_exc_exc = 0.005
weight_exc_inh = 0.005
weight_inh_exc = 0.5
delay = 3.0
rng_seed = 42
stimulus_onset = 25.0
stimulus_sigma = 0.5
runtime = 150.0


# --- Configure the simulator/hardware ---------

sim.setup(timestep=0.1)


# --- Create populations of neurons ------------

populations = {'exc': [], 'inh': []}
for syn_type in ('exc', 'inh'):
    populations[syn_type] = [sim.Population(population_size, sim.IF_cond_exp, neuron_parameters)
                             for i in range(n_populations)]


# --- Connect the populations in a chain -------

connector_exc_exc = sim.AllToAllConnector(weights=weight_exc_exc, delays=delay)
connector_exc_inh = sim.AllToAllConnector(weights=weight_exc_inh, delays=delay)
connector_inh_exc = sim.AllToAllConnector(weights=weight_inh_exc, delays=delay)

for i in range(n_populations):
    j = (i + 1) % n_populations
    prj_exc_exc = sim.Projection(populations['exc'][i], populations['exc'][j],
                                 connector_exc_exc, target='excitatory')
    prj_exc_inh = sim.Projection(populations['exc'][i], populations['inh'][j],
                                 connector_exc_inh, target='excitatory')
    prj_inh_exc = sim.Projection(populations['inh'][i], populations['exc'][i],
                                 connector_exc_exc, target='inhibitory')

# --- Create and connect stimulus --------------

numpy.random.seed(rng_seed)
stim_spikes = numpy.random.normal(loc=stimulus_onset, scale=stimulus_sigma, size=population_size)
stim_spikes.sort()
stimulus = sim.Population(1, sim.SpikeSourceArray, {'spike_times': stim_spikes})

prj_stim_exc = sim.Projection(stimulus, populations['exc'][0],
                              connector_exc_exc, target='excitatory')
prj_stim_inh = sim.Projection(stimulus, populations['inh'][0],
                              connector_exc_inh, target='excitatory')


# --- Set-up recording -------------------------

for syn_type in ('exc', 'inh'):
    for population in populations[syn_type]:
        population.record()


# --- Run the simulation -----------------------

sim.run(runtime)


# --- Plot spike raster ------------------------

colours = {'exc': 'r', 'inh': 'b'}

id_offset = 0
for syn_type in ['exc', 'inh']:
    for population in populations[syn_type]:
        spikes = population.getSpikes()
        colour = colours[syn_type]
        plt.plot(spikes[:,1], spikes[:,0] + id_offset,
                 ls='', marker='o', ms=1, c=colour, mec=colour)
        id_offset += population.size

plt.xlim((0, runtime))
plt.ylim((-0.5, 2* n_populations * population_size + 0.5))
plt.xlabel('time (t)')
plt.ylabel('neuron index')
plt.savefig("synfire_chain.png")
