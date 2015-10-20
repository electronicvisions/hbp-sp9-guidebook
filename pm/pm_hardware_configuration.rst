.. _nmpm1-hardware-configuration:

======================
Hardware configuration
======================

.. _nmpm1-hardware-figure:

.. figure:: nmpm1_cgiracks.jpg
      :width: 100%
      :alt: NMPM-1 system

      The NM-PM-1 system: five 19-inch racks contain 20 neuromorphic wafer modules (cf. :num:`waferscale-hardware-figure`), the other two racks carry power supplies and a conventional control cluster.

At the core of the NM-PM-1 wafer-scale hardware system (see Figure :num:`waferscale-hardware-figure`) is an uncut wafer built from mixed-signal ASICs [#f1]_,
named `High Input Count Analog Neural Network` chips (`HICANNs`), that provide a highly configurable substrate which physically emulates adaptively spiking neurons and dynamic synapses (`Schemmel et al. (2010)`_, `Schemmel et al. (2008)`_).
The intrinsic time constants of these VLSI model circuits are multiple orders of magnitude shorter than their biological originals.
Consequently, the hardware model evolves with a speedup factor of :math:`10^3` up to :math:`10^5` compared to biological real time, the precise value depending on the configuration of the system.
This speedup enables power-efficient computation as the energy consumption for synaptic transmissions is several orders of magnitude lower than in classically simulated neuronal networks.

.. _waferscale-hardware-figure:

.. figure:: waferscale_system.png
      :width: 100%
      :alt: wafer-scale system
    
      The NM-PM-1 wafer-scale hardware system: Wafer comprising HICANN building blocks and on-wafer communication infrastructure, mechanical infrastructure (top cover and insertion frame), analog readout boards (AnaB), power supply and digital inter-wafer as well as wafer-host communication modules.

In addition to a high-bandwidth asynchronous on-wafer event communication infrastructure, 48 FPGA communication modules provide off-wafer connectivity (to other wafers and to host computers).

A full wafer system comprises 384 interconnectable HICANNs, each of which implements more than 114,688 programmable dynamic synapses and up to 512 neurons, resulting in a total of approximately 44 million synapses and up to 196,608 neurons per wafer module.
The exact number of neurons depends on the configuration of the substrate, which allows to combine multiple neuron building blocks to increase the input count per cell.

Via the communication FPGAs the system can be configured and operated from a host computer.
Each communication FPGA is connected to a dedicated area on the wafer which contains 8 HICANNs.
This FPGA-HICANN link is used to configure the HICANNs as well as to transmit pulse events to and from the neural circuits on the wafer.
The pulse communication between the on-wafer neurons is performed by a bus-like network directly on the wafer.

The system provides a high degree of configurability with respect to network architecture and neuron parameters:

  * each neuron provides configurable AdEx neuron dynamics
  * the synapses provide 4-bit weight resolution and STDP functionality
  * the connection topology can be configured

For a detailed specification see HBP deliverable `D9.7.1`_.

.. _D9.7.1: https://flagship.kip.uni-heidelberg.de/jss/FileExchange?s=qqdXDg6HuX3&uID=65

.. _nmpm1-overview-figure:

.. figure:: nmpm1_overview.png
      :width: 100%
      :alt: Simplified overview of the NM-PM1 system

      The left area illustrates the partitioning of HICANNs into larger units (reticles) and the data flow up to the control cluster.

Figure :num:`nmpm1-overview-figure` provides a simplified overview of the NM-PM1 system.
The support infrastructure is responsible for power supply, off-wafer communication and analog readout functionality.
A dedicated Raspberry Pi embedded computer monitors and controls all power links as well as other operating parameters of the wafer system.
Analog readout (e.g., recording of membrane voltages) functionality is provided by a custom analog readout module (AnaRM).
Several AnaRMs are handled by another dedicated control computer.
The control/compute cluster orchestrates the configuration of the system and the execution of neuronal network experiments including all input and output data of the emulated network.
All hardware resources (neuromorphic and support hardware as well as conventional compute resources) are managed by `SLURM`_.

.. _SLURM: http://slurm.schedmd.com

.. [#f1] Application Specific Integrated Circuit
.. [#f2] Field Programmable Gate Array

Supported cells and plasticity mechanisms
=========================================

The :mod:`pyNN.hardware.hbp_pm` module supports the following neuron and synapse models:

  * :class:`EIF_cond_exp_isfa_ista` (adaptive exponential integrate-and-fire model, conductance-based synapses)
  * :class:`IF_cond_exp` (leaky integrate-and-fire model, conductance-based synapses)
  * :class:`SpikeSourceArray` (emits spikes with an explicit list of spike times)
  * :class:`SpikeSourcePoisson` (emits spikes with spike times according to a Poisson process)
  * :class:`TsodyksMarkramMechanism` (short-term synaptic plasticity according to the model of Markram et al., 1998)

The hardware version of :class:`TsodyksMarkramMechanism` is slightly modified (cf. Schemmel et al. 2007, 2006): it cannot implement depression and facilitation at the same time.
The basic functionality stays the same, however; in the PyNN script, one has to set one of the model’s time constants ``tau_rec`` and ``tau_facil`` to 0, opting for either depression or facilitation.


Parameter ranges
================

The NM-PM-1 wafer-scale hardware has a wide but still limited range for neuron, synapse and stimulus parameters.
The ``pyNN.hardware.hbp_pm`` back-end automatically does a rough range-checking already in the Python domain, thereby giving immediate feedback to the user. The precise range limits depend on the system calibration, so the actual ranges may be slightly smaller or larger than given here.

.. TODO: the following ranges are out of date. After update, uncomment the following text.
.. The default ranges for the :class:`IF_cond_exp` are:
..
   ==========  =======  =======  =======
   Parameter   Default  Min      Max
   ==========  =======  =======  =======
   tau_refrac  0.1      0.0      10.0
   cm          1.0      0.2      0.2
   tau_syn_E   5.0      0.5      5.0
   v_rest      -65.0    -50.0    -50.0
   tau_syn_I   5.0      0.5      5.0
   tau_m       20.0     9.0      110.0
   e_rev_E     0.0      0.0      0.0
   i_offset    0.0      0.0      0.0
   e_rev_I     -70.0    -100.0   -100.0
   v_thresh    -50.0    -100.0   0.0
   v_reset     -65.0    -100.0   0.0
   ==========  =======  =======  =======
   
   .. todo:: comment on the fact that in several cases the default is outside the allowed range. Also, why is the range for v_rest [-50, -50]? Should also comment on the unphysiological value for e_rev_I.
   
   
   Some configuration options can modify these ranges. With ``speedUpFactor = 1000``, the ranges for all parameters with dimension time are modified:
   
   ==========  =======  =======  =======
   Parameter   Default  Min      Max
   ==========  =======  =======  =======
   tau_refrac  0.1      0.0      1.0
   tau_syn_E   5.0      0.1      0.5
   tau_syn_I   5.0      0.1      0.5
   tau_m       20.0     0.9      11.0
   ==========  =======  =======  =======
   
   With ``useSmallCap = True``, only the range of `tau_m` is modified:
   
   ==========  =======  =======  =======
   Parameter   Default  Min      Max
   ==========  =======  =======  =======
   tau_m       20.0     0.7      8.3
   ==========  =======  =======  =======


As noted above, the parameter ranges given here are updated with the latest results from calibration,
so the actual allowed ranges may be slightly different.
The hardware will generate a :class:`ParameterValueOutOfRangeError` if any parameter is outside its range, for example:

.. code-block:: python

    import pyNN.hardware.hbp_pm as sim
    sim.setup()
    neurons = sim.Population(10, sim.IF_cond_exp, cellparams={'tau_refrac': 30.0})


.. code-block:: python

    Traceback (most recent call last):
        [...]
    range_checker.ParameterValueOutOfRangeError:
        30.0 is out of the range supported by the hardware
        (valid range for parameter tau_refrac is: (0.16, 20.0))


Recording spikes and membrane potential
=======================================

The spikes of all neurons mapped onto the hardware as well as the input spikes can be recorded.
Spikes are returned to Python via the standard PyNN interface (i.e. the :func:`getSpikes()` and :func:`printSpikes()` methods of the :class:`Population` class for PyNN 0.7, and :func:`get_data()` and :func:`write_data()` for PyNN 0.8).

At present, it is not possible to obtain membrane potential recordings from the real hardware through the PyNN interface, this requires direct access to the hardware.
However, when running simulation with the ESS, membrane potential recording and retrieval is available via the standard PyNN interface.


Initialization of state variables
=================================

As the hardware runs continuously and cannot be "stopped", state variables for neuron and synapse models can not be initialized.
Calls like the following :func:`initalize()` have no effect.

.. code-block:: python

    neurons = sim.Population(10, sim.IF_cond_exp)
    neurons.initialize('v', -65.0)
        # initialize all voltages to -65 mV, has no effect on hardware


Injected current
================

In general, the NM-PM-1 wafer-scale hardware does not support PyNN ``CurrentSources``.
There is, however, a very limited number of periodic current sources, which can be used for debugging and examination of single hardware neurons.
See :ref:`periodic_current_sources` in the appendix for details.


Projections
===========

Currently, synaptic delays are not configurable from PyNN, as adjustable delays are currently not available on the NM-PM-1 hardware.
Synaptic delays lie within a range of 1-4 ms when running with a speedup factor of 10000.
The exact value depends on the ongoing activity and on the distance between neurons on the neuromorphic wafer-scale hardware.
Hence the values for the delay parameter are ignored for all ``Projection`` or ``connect()`` calls.

The API support for :class:`Projection` is currently limited.
Synaptic parameters cannot be changed after the instantiation of a :class:`Projection`,
nor can the parameter values be read back: none of the :func:`getX()`, :func:`randomizeX()`, or :func:`setX()` methods of Projections work.


Synapse and neuron loss
=======================

On the hardware the resources for neurons and synapses are limited.
The number of available hardware neurons and synapses depends on the chosen hardware setup and the hardware neuron size, see below.
Furthermore, it can happen that some synapses from the PyNN model can not be realized on the hardware, as they are ''lost'' during the mapping process.
The reason for that can be limited configurability of the hardware circuits, or non-optimal algorithms for the very-complex mapping process.
More details on the sources of synapse loss and compensation techniques can be found in `Petrovici et al. (2014)`_.

The user can specify the maximum allowed neuron and synapse loss for a given network with the following arguments to the :func:`setup()` function::

    maxSynapseLoss - maximum synapse loss allowed during mapping.
                     default: 0.0
                     range: (0.0, 1.0)
    maxNeuronLoss  - maximum neuron loss allowed during mapping.
                     default: 0.0
                     range: (0.0, 1.0)

Here, synapse/neuron loss refers to the fraction of synapses/neurons, that can not be mapped onto the hardware.
By specifying this limit, the user can avoid experiments where the too many synapses or neurons are lost. By default, the mapping stops if any neuron or synapse can not be mappped.


Changing the number of incoming synapses per neuron
===================================================

Each HICANN has 512 neuron circuits (`DenMems`) implementing the `AdEx` neuron model, and each `DenMem` has 224 incoming synapses. One can combine several `DenMems` to build larger neurons with more incoming synapses; of course, this reduces the overall number of neurons.

The number of hardware neurons (`DenMems`) per neuron, and thus the number of neurons per HICANN, can be controlled via the setup parameter ``hardwareNeuronSize``.

.. code-block:: python

    pynn.setup(hardwareNeuronSize=1)

The following table shows how the parameter ``hardwareNeuronSize`` controls the effective number of neurons per HICANN and the number of incoming synapses per neuron:

======================  ==============  ===============
``hardwareNeuronSize``  Neurons/HICANN  Synapses/Neuron
======================  ==============  ===============
1                       472               224
2                       236               448
4                       118               896
8                       59                1792
16                      32                3584
32                      16                7168
64                      8                 14336
======================  ==============  ===============

By default a hardware neuron size of 1 is used.

.. note:: Why is the effective number of neurons smaller than 512 divided by ``hardwareNeuronSize`` for values up to 8?

          This is due to a technical limitation: Up to 64 neuron inject their
          pulses into a on-wafer routing bus. Each neuron then has a neuron
          address between 0-63 on that bus. Address 0 can not be used by normal
          neurons, as it is required for a background event generator, which
          continuously sends pulses over the routing buses in order to keep
          asynchronous buses "locked". When a pulse with the given 6-bit
          address enters a synapse array, for each synapse it is checked
          whether the pulse address matches a configured address per synapse.
          As there is no extra bit to disable a hardware synapse, this has to
          be done with the address: The synapse has to be configured with an
          address that never arrives. For each block of 16 addresses ( [0-15],
          [16-31], [32-47], [48-63] ), one address needs to be reserved for
          disabling the synapse.
          Hence there are only 59 Addresses per bus that can be used per routing bus.

.. move this note to a technical appendix?


Multiple runs
=============

The hardware backend allows multiple calls of :func:`run()`.
The only variables you can change after :func:`run()` has been called for the first time are the input spiketrains of spike sources.

What **cannot** be done after the first run is the following:

* create new neurons;
* create new connections;
* change synapse or neuron parameters;
* change the recording configuration.

After each run, you need to call :func:`reset()` to set the simulation time back to 0 and clear the recorded data.
It is not possible to call :func:`run()` several times without calling :func:`reset()` in between.
This is different to software simulators, where the simulation time is accumulated and the states (membrane potential etc.) are preserved for the next run.
In contrast, on the hardware, the analog states can not be preserved, so that multiple runs without :func:`reset()` in between make no sense.
Calling :func:`getSpikes()` or :func:`printSpikes()` returns only the spikes from the latest run.

.. note:: For multiple runs there is an option to program floating gates only once: just set ``sim.setup(programFloatingGates="once")`` (this is the default).

**Example:**

For a full example see `example_single_neuron_l2_input_multiple_runs`_.
where the I-O frequency Curve of a neuron is measured with this option.

.. _example_single_neuron_l2_input_multiple_runs: https://gitviz.kip.uni-heidelberg.de/projects/mappingtool/repository/entry/misc/tests/examples/single_neuron_l2_input/single_neuron_l2_input_multiple_runs.py


Available hardware setups
=========================

By default, each job run on the PM facility is assigned to a single wafer,
but it is also possible to have more fine grained control over which parts of the hardware to use.
This is specified using the ``hardware`` argument to the :func:`setup()` function, for example:

.. code-block:: python

    import pyNN.hardware.hbp_pm as sim
    sim.setup(hardware=sim.hardwareSetup['one-wafer])


The ``hardware`` argument should be a list of setups, where each setup is specified by a dictionary with the following parameters:

``setup``
   specifies the type of the hardware, either 'vertical_setup' or 'wafer'

``wafer_id``
   the logical id of the wafer in the calibration database [default: 0]

``hicannIndices``
   a list of HICANN Indices (HALBE Enumeration) to use for mapping.
   If not specified, all HICANNs of the wafer will be used. Default: range(384)

``setup_params`` - a dictionary specifying the parameters of the hardware setup

   ``ip`` - IP Address (v4) of FPGA of vertical setup as string in dotted decimal form.

      Only used if setup is a 'vertical_setup'. Default: 192.168.1.1

   ``num_hicanns`` - number of HICANNs in the JTAG chain of vertical setup

      Default: 1
      Range: (1, 8)

There are several predefined hardware setups in the dictionary ``pyNN.hardware.hbp_pm.hardwareSetup``.

As mentioned above, one can choose from different predefined hardware setups via:

.. code-block:: python

    sim.setup(hardware=sim.hardwareSetup[<SETUP>])

Here are the details about the different hardware setups:

=================  ==========  ========
``hardwareSetup``  `#HICANNs`  geometry
=================  ==========  ========
one-hicann         1
one-reticle        8           4x2
small              32          8x4
medium             128         16x8
medium2            128         32x4
large              240         20x12
large2             224         28x8
one-wafer          384         WaferMap_
=================  ==========  ========

By default a complete wafer (i.e. ``one-wafer``) is used.
When using the ESS simulator it is strongly recommended to choose a smaller hardware setup to reduce the simulation time.

The following table shows the **total number of neurons** depending on the ``hardwareNeuronSize`` and the ``hardwareSetup``

===============  ======  =====  =====  =====  =====  ====  ====
`hardwareSetup`            `hardwareNeuronSize`
---------------  ----------------------------------------------
..               1       2      4      8      16     32    64
===============  ======  =====  =====  =====  =====  ====  ====
'one-hicann'     472     236    118    59     32     16    8
'one-reticle'    3776    1888   944    472    256    128   64
'small'          15104   7552   3776   1888   1024   512   256
'medium'         60416   30208  15104  7552   4096   2048  1024
'medium2'        60416   30208  15104  7552   4096   2048  1024
'large'          113280  56640  28320  14160  7680   3840  1920
'large2'         105728  52864  26432  13216  7168   3584  1792
'one-wafer'      181248  90624  45312  22656  12288  6144  3072
===============  ======  =====  =====  =====  =====  ====  ====

Input Bandwidth Limits
======================

The bandwidth for external simulus spikes (from :class:`SpikeSourcePoisson` and :class:`SpikeSourceArray`) is limited on the hardware.
The following table lists the maximum input bandwidth for a speedup factor of 10000:

=============   ==============
hardwareSetup   Input BW [kHz]
=============   ==============
one-hicann      2.083
one-reticle     12.5
small           37.5
medium          100.0
medium2         100.0
large           150.0
large2          112.5
one-wafer       150.0
=============   ==============


Configuration summary
=====================

The hardware is configured by passing arguments to the :func:`setup()` function.
Most of these options have been discussed above. We summarize them here for reference.
These arguments will be ignored by other PyNN backends.

``speedupFactor``
    Determines how much faster the emulation on the hardware takes place compared to biological real time. Default: 10000.
    Note that changing the speedup factor also scales the neuron and synapse parameter ranges.

``useSmallCap``
    For the hardware neuron one has the choice from two different capacitors used as the membrane capacitance.
    By default the big capacitor with 2.165 pF is used.
    By setting ``useSmallCap=True`` one can switch to the small capacitance with 0.164 pF.
    Then, the parameter ranges of the membrane time constant ``tau_m``, the adaption variables ``a`` and ``b`` and synaptic weights are updated.
    This option is useful when running at a high speedup factor (e.g. 20000).

.. warning:: Note that there is currently no calibration data available for the small capacitance, such that hardware experiments are not expected to use a precise transformation of neuron parameters to the hardware.

``maxSynapseLoss``
    Maximum synapse loss allowed during mapping (range 0-1). The default is zero (loss of synapses will halt the mapping process).

``maxNeuronLoss``
    Maximum neuron loss allowed during mapping (range 0-1). The default is zero (loss of neurons will halt the mapping process).

``hardware``
    Specifies which parts of the hardware to use. See the section "Available hardware setups" above.

``hardwareNeuronSize``
    Specifies the size of hardware neurons, i.e. the number of neuron circuits that are used to form a larger neuron.
    The higher this number, the higher is the number of incoming synapses per neuron, and the lower is the total
    number of neurons. Default: 1. Choices: [1, 2, 4, 8, 16, 32, 64]

``programFloatingGates``
   When performing multiple runs, this option determines whether the "floating gates" which hold the parameter values should
   be reprogrammed for each run, or only once. Default: 'always'. Choices: ['always', 'once']

``rng_seeds``
   A list of seeds used for certain sources of randomness (e.g. Poisson spike trains).


.. todo:: discuss when people might want to/need to change the default hardware setup.


.. include:: using_pm_newflow.rst_tochide


.. _`Petrovici et al. (2014)`: http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0108590
.. _`Schemmel et al. (2010)`: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5536970&isnumber=5536941
.. _`Schemmel et al. (2008)`: http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4633828 
.. _WaferMap: http://129.206.127.67/jss/WaferMapShow?scale=1.0&theta=1.5709999799728394&waferNumber=1&drawMode=DRAW_MODE_HICANN_ConfigID
