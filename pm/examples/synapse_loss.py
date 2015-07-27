#!/usr/bin/env python
"""
example script for extracting synapse loss after mapping
"""

from pymarocco import PyMarocco
import pyhmf as pynn
import numpy as np
import pylogging
pylogging.reset()
pylogging.default_config(level=pylogging.LogLevel.ERROR)

def projectionwise_synapse_loss(proj, marocco):
    """
    computes the synapse loss of a projection
    params:
      proj    - a pyhmf.Projection
      marocco -  the PyMarocco object after the mapping has run.

    returns: (nr of lost synapses, total synapses in projection)
    """
    orig_weights = proj.getWeights(format='array')
    mapped_weights = marocco.stats.getWeights(proj)
    syns = np.where(~np.isnan(orig_weights))
    realized_syns = np.where(~np.isnan(mapped_weights))
    orig = len(syns[0])
    realized = len(realized_syns[0])
    print "Projection-Wise Synapse Loss", proj, (orig - realized)*100./orig
    return orig-realized, orig

def plot_projectionwise_synapse_loss(proj, marocco):
    """
    plots the realized and lost synapses of a projection
    params:
      proj    - a pyhmf.Projection
      marocco -  the PyMarocco object after the mapping has run.
    """
    orig_weights = proj.getWeights(format='array')
    mapped_weights = marocco.stats.getWeights(proj)
    realized_syns = np.where(np.isfinite(mapped_weights))
    lost_syns = np.logical_and(np.isfinite(orig_weights), np.isnan(mapped_weights))

    conn_matrix = np.zeros(orig_weights.shape)
    conn_matrix [ realized_syns ] =  1.
    conn_matrix [ lost_syns ] = 0.5

    import matplotlib.pyplot as plt
    plt.figure()
    plt.subplot(111)
    plt.imshow(conn_matrix,cmap='hot',interpolation='nearest')
    plt.xlabel("post neuron")
    plt.ylabel("pre neuron")
    plt.title("realized and lost synapses")
    plt.show()

def main():
    """
    create small network with synapse loss.  The synapse loss happens due to a
    maximum syndriver chain lenght of 5 and only 4 denmems per neuron.  After
    mapping, the synapse loss per projection is evaluated and plotted for one
    projection.  The sum of lost synapses per projection is compared to the
    overall synapse loss returnd by the mapping stats.
    """
    marocco = PyMarocco()
    marocco.placement.setDefaultNeuronSize(4)
    marocco.routing.syndriver_chain_length = 5

    pynn.setup(marocco=marocco)

    neuron = pynn.Population(50, pynn.IF_cond_exp)
    source = pynn.Population(50, pynn.SpikeSourcePoisson, {'rate' : 2})

    connector = pynn.FixedProbabilityConnector(
            allow_self_connections=True,
            p_connect=0.5,
            weights=0.00425)
    proj_stim = pynn.Projection(source, neuron, connector, target="excitatory")
    proj_rec = pynn.Projection(neuron, neuron, connector, target="excitatory")

    pynn.run(1)

    print marocco.stats

    total_syns = 0
    lost_syns = 0
    for proj in [proj_stim, proj_rec]:
        l,t = projectionwise_synapse_loss(proj, marocco)
        total_syns += t
        lost_syns += l

    assert total_syns == marocco.stats.getSynapses()
    assert lost_syns == marocco.stats.getSynapseLoss()

    plot_projectionwise_synapse_loss(proj_stim, marocco)
    pynn.end()

if __name__ == "__main__":
    main()
