==========================
Using the SpiNNaker system
==========================

As explained in :ref:`building_models`, both the experiment description and the model description
for the SpiNNaker system must be written as Python scripts,
using the PyNN application programming interface (API), version 0.8.
The implementation of the `PyNN 0.8 API http://neuralensemble.org/docs/PyNN/0.8/api_reference.html`__ for the SpiNNaker system is called :py:mod:`sPyNNaker8`, and
is also available as the module :py:mod:`pyNN.spiNNaker`:


.. code-block:: python

    import pyNN.spiNNaker as sim

Supported PyNN functionality
============================

:py:mod:`sPyNNaker` currently supports a subset of the standard PyNN 0.8 API together with a number of extensions.
The supported interface functions are listed below.
A possibly more up-to-date list can be found in the `online documentation <http://spinnakermanchester.github.io/latest/spynnaker_limitations.html>`__.

In the next planned release, support for the PyNN 0.9 API will be included.

Neuron model limitations
------------------------

sPyNNaker currently supports the following model types:

:py:class:`IF_curr_exp`
  Current based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron

:py:class:`IF_cond_exp`
  Conductance based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron

:py:class:`IF_curr_alpha`
  Conductance based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron

:py:class:`Izhikevich`
  Current based Izhikevich with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron

Note that there are also further restrictions on what plasticity types are supported when used with the above models.

All of our neural models have a limitation of 255 neurons per core. Depending on which SpiNNaker board you are using, this will limit the number of neurons that can be supported in any simulation.

External input
--------------

sPyNNaker currently supports :py:class:`SpikeSourceArray`
(note that the spikes to be input can be changed between calls to run) and
:py:class:`SpikeSourcePoisson`.

Currently, only the ``i_offset`` parameter of the neural models can be used to inject current directly;
there is no support for noisy or step-based current input.

A third, non-standard PyNN interface, way of injecting current into a PyNN simulation executing on the hardware is through live injection from an external device.
These functions are supported by our :py:class:`sPyNNakerExternalDevicesPlugin`.
A description on how to use this functionality can be found `here <http://spinnakermanchester.github.io/latest/spynnaker_external_io.html>`_.

Connectors
----------

sPyNNaker currently supports the following standard connector types:

- :py:class:`OneToOneConnector`
- :py:class:`AllToAllConnector`
- :py:class:`FixedNumberPreConnector`
- :py:class:`FixedNumberPostConnector`
- :py:class:`FixedTotalNumberConnector`
- :py:class:`FixedProbabilityConnector`
- :py:class:`DistanceDependentProbabilityConnector`
- :py:class:`FromFileConnector`
- :py:class:`FromListConnector`

Note that using the latter two connectors will result in slower operation of the tools.


Plasticity
----------

sPyNNaker currently only supports plasticity described by an :py:class:`STDPMechanism`.

sPyNNaker supports the following STDP timing dependence rules:

- :py:class:`SpikePairRule`

and the following STDP weight dependence rules:

- :py:class:`AdditiveWeightDependence`
- :py:class:`MultiplicativeWeightDependence`

Simulation execution
--------------------

sPyNNaker supports the ability to call :py:func:`run()` multiple times with different combinations of runtime values,
and to call :py:func:`reset()` multiple times with :py:func:`run()` interleaved.

sPyNNaker supports the addition of :py:class:`Population`\s and :py:class:`Projection`\s between a :py:func:`reset()` and a :py:class:`run()`,
but not between multiple calls to run().

PyNN missing functionality
--------------------------

sPyNNaker does not support:

- :py:class:`Assembly`.

sPyNNaker does not support changing of weights / delays / neuron parameters between the initial call to :py:class:`run()` and a :py:func:`reset()` call.

Parameter ranges
----------------

All parameters and their ranges are under software control.

Weights are held as 16-bit integers, with their range determined at compile-time to suit the application; this limits the overall range of weights that can be represented, with the smallest representable weight being dependent on the largest weights specified.

There is a limit on the length of delays of between 1 and 144 time steps (i.e. 1 - 144 ms when using 1 ms time steps, or 0.1 - 14.4 ms when using 0.1 ms time steps). Delays of more than 16 time steps require an additional "delay population" to be added; this is done automatically by the software when such delays are detected.

Membrane voltages and other neuron parameters are generally held as 32-bit fixed point numbers in the s16.15 format. Membrane voltages are held in mV.

Synapse and neuron loss
-----------------------

Projection links between two sub-populations that were initially defined as connected are removed by the software if the number of connections between the two sub-populations is determined to be zero when the projection is realised in the software’s mapping process.

The SpiNNaker communication fabric can drop packets, so there is the chance during execution that spikes might not reach their destination (or might only reach some of their destinations). The software attempts to recover from such losses through a reinjection mechanism, but this will only work if the overall spike rate is not so high as to overload the communications fabric in the first place.


Mapping and Routing
===================

The mapping process examines the neural network definition and attempts to break it down in to parts, each of which can be executed on a SpiNNaker core.  A routing algorithm is then run to work out the communication paths between the cores on the SpiNNaker network.  In the current software, mapping and routing takes place on the host machine as part of the placement and configuration manager (PACMAN).

It is possible for end users to add their own mapping and routing algorithms into the tool chain.  Instructions on how to do so can be found `here <http://spinnakermanchester.github.io/latest/mapping_algorithms.html>`__.
