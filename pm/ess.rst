===================================
Simulating the BrainScaleS hardware
===================================

The Executable System Specification (ESS) is a software model of the BrainScaleS hardware system.
The ESS is implemented in C++/SystemC and contains functional models of all relevant units of the wafer-scale hardware.
It is fully executable and resembles how neural experiments are run on the real wafer-scale system.

The ESS allows offline experimentation with the BrainScaleS system, and can be used for testing
small models locally before submitting them to the hardware system, and for introspecting the
system behaviour. The ESS supports PyNN versions 0.7 and 0.8.

Note, however, that the ESS runs *much* more slowly than the real hardware.

.. include:: ess_docker.rst_tochide

Using the ESS
=============

Scripts to run on the ESS should in general be identical to those that run on the BrainScaleS hardware. The only required
difference is to choose ``PyMarocco.ESS`` as the PyMarocco backend.

Example
```````

A full example where an Adaptive-Exponential Integrate & Fire neuron is stimulated by external spikes, is shown in ``nmpm1_adex_neuron_ess.py``:

.. literalinclude:: examples/sw/nmpm1_adex_neuron_ess.py

Note that the same script runs also with ``pyNN.nest``, just change the first line that imports the PyNN backend.

ESS Config
``````````

In addition, one can specify an ESS configuration as follows:

.. code-block:: python

    import pysthal

    marocco = PyMarocco()
    marocco.backend = PyMarocco.ESS

    ess_config = pysthal.ESSConfig()
    ess_config.enable_weight_distortion = True
    ess_config.weight_distortion = 0.2
    ess_config.pulse_statistics_file = "pulse_stats.py"

    marocco.ess_config = ess_config

parameters of ``ESSConfig``:

``enable_weight_distortion``
   Enables the distortion of synaptic weights in the virtual hardware system.

   This option can be used to resemble the fixed pattern noise of synaptic
   weights on the real hardware.

   Default: ``False``


``weight_distortion``
   Specifies the distortion of synaptic weights in the virtual hardware system.

   This parameter defines the fraction of the original value, that is used as
   the standard deviation for randomizing the weight according to a normal
   distribution around the original value.
   All weights are clipped to positive values.

   Default: ``0.0``

``pulse_statistics_file``
    Name of file to which the ESS pulse statistics are written.

    See `Pulse Loss Statistics`_ for details.

    Default: ``""``


Pulse Loss Statistics
`````````````````````

The ESS allows to count all spikes that were lost in any place of the virtual hardware system.
Spikes are mostly lost in the off-wafer communication network (also called ''Layer 2 network'') that connects the wafer to the host PC.
In the Layer 2 network pulse loss can happen on two routes:

1. Stimulation:
   not all spikes from the spike sources (:class:`SpikeSourcePoisson` or :class:`SpikeSourceArray`) are delivered to its targets, because the bandwidth in the off-wafer network is limited. When a spike is lost, it is lost for its targets.

2. Recording:
   For the same bandwidth constraints in the off-wafer network, some spikes of real neurons can be lost on the route from the wafer to the FGPGAs, Hence, in the received spike data some events are missing.
   However, the 'non-recorded' spikes did reach their target neurons on the wafer.

Spikes can also be lost on the wafer, but only in rare cases when many neuron located on the same HICANN fire synchronously.

3. On-wafer Spike Loss:
   This is the case of pulses lost in the on-wafer pulse-communication system (also called `Layer 1 network`). If this happens, spikes are completely deleted, and reach no other neuron.

4. Spike Drop before Simulation:
   The playback module of the FPGA, which plays back the stimuli pulses at given times, also has a limited bandwidth. This limitation is considered beforehand, such that spikes are dropped even before the simulation, in order to avoid a further delaying of many more spikes during an experiment.

The ESS counts the lost and sent pulses.
After the simulation, you will see something in the log for a loglevel>=2::

    INFO  Default *************************************
    INFO  Default LostEventLogger::summary
    INFO  Default Layer 2 events dropped before sim : 837/3939 (21.249 %)
    INFO  Default Layer 2 events lost :               243/3199 (7.59612 %)
    INFO  Default Layer 2 events lost downwards :     243/3102 (7.83366 %)
    INFO  Default Layer 2 events lost upwards   :     0/97 (0 %)
    INFO  Default Layer 1 events lost : 0/79 (0 %)
    INFO  Default *************************************


You can specify to get this data by specifying a file ``pulse_statistics_file``
in the `ESS Config`_:

.. code-block:: python

    marocco.ess_config.pulse_statistics_file = "pulse_stats.py"
    sim.setup(marocco=marocco)


Then the pulse statistics file contains a Python dictionary
``pulse_statistics`` which can be use for further processing:

.. code-block:: python

    pulse_statistics = {
    'l2_down_before_sim': 3939,
    'l2_down_dropped_before_sim': 837,
    'l2_down_sent': 3102,
    'l2_down_lost': 243,
    'l2_up_sent': 97,
    'l2_up_lost': 0,
    'l1_neuron_sent': 79,
    'l1_neuron_lost': 0,
    }

