===============
Building models
===============

.. contents::
   :local:


The Neuromorphic Computing Platform executes experiments performed on computational models of neuronal networks.

Both the experiment description and the model description must be written as Python scripts, using the PyNN_ API.

At the time of writing, both the NM-PM-1 and NM-MC-1 systems implement version 0.7 of the PyNN API.

  | `PyNN 0.7 documentation`_

The simulator of the NM-PM-1 hardware ('ESS') supports both versions 0.7 and 0.8.

  | `PyNN 0.8 documentation`_


NM-PM-1 system
==============

This section contains information specific to the `pyNN.hardware.hbp_pm` backend

Transfer material from http://neuralensemble.org/trac/PyNN/wiki/NeuromorphicHardwareFAQ

Standard PyNN interface
-----------------------

Supported Standard Cells
````````````````````````

In the current state, the :mod:`pyNN.hardware.hbp_pm` module supports two neuron types and two types
of external spike sources. The parameters for all models are constrained to the parameters available from the chip.
See "RangeChecker" below.

`EIF_cond_exp_isfa_ista`:
   Adaptive-Exponential integrate-and-fire model (Brette and Gerstner, 2005) with exponential decaying conductances.

`IF_cond_exp`:
   Leaky integrate-and-fire model with exponential decaying conductances.

`SpikeSourceArray`:
   Creates a spike train, i.e. a list of spike times.

`SpikeSourcePoisson`:
   Creates a spike train with a Poisson distribution with a given mean-rate in a defined time interval.


Supported Plasticity Mechanisms
```````````````````````````````

Short Term Plasticity: `TsodyksMarkramMechanism`:

Among others, PyNN supports the short-term plasticity mechanism presented in Markram et al. (1998).
The NM-PM-1 Hardware implements a slightly modified version of it (cf. Schemmel et al. 2007, 2006): it cannot implement depression and facilitation at the same time.
The basic functionality stays the same, however, in the PyNN script, one has to set one of the model’s time constants `tau_rec` and `tau_facil` to 0, opting for depression or facilitation.

.. warning:: The Short Term Plasticity is currently only functional with the executable system specification(ESS), the support for the real system is coming soon.

Hardware-Specific Constraints
-----------------------------

Stimulation and Recording
`````````````````````````

**Spikes**:
   The spikes of all neurons mapped onto a HICANN as well as the input spikes can be recorded. Spikes are automatically returned to the python world via the standard pyNN interface.

**Voltages**:
   Currently, the voltage recording method `record_v` triggers to enable the analog output of up to two neurons, which then can be examined with an oscilloscope. No voltage traces are returned to the PyNN domain.

Hardware Parameter Ranges
`````````````````````````

The NM-PM-1 wafer-scale hardware has a wide but still limited range for neuron, synapse and stimulus parameters.
The `pyNN.hardware.hbp_pm` back-end automatically does a rough range-checking already in the python domain, thereby giving immediate feedback to the user.
The parameter ranges used here are updated with the latest results from calibration.
See the following example and crash report:

.. code-block:: python

    import pyNN.hardware.hbp_pm as sim
    sim.setup()
    Neurons = sim.Population(10, sim.IF_cond_exp, cellparams={'tau_refrac': 30.0})


.. code-block:: python

    Traceback (most recent call last):
      File "range_check_example.py", line 3, in <module>
        Neurons = sim.Population(10,sim.IF_cond_exp, cellparams={'tau_refrac':30.})
      File "/home/vogginger/project/symap2ic/components/pynnhw/src/hardware/brainscales/population.py", line 86, in __init__
        common.Population.__init__(self,size,cellclass,cellparams,structure,label)
      File "/home/vogginger/opt/lib64/python2.7/site-packages/pyNN/common.py", line 892, in __init__
        self.celltype = cellclass(cellparams)
      File "/home/vogginger/project/symap2ic/components/pynnhw/src/hardware/brainscales/cells.py", line 140, in __init__
        self.checkParameterRanges(checked_params)
      File "/home/vogginger/project/symap2ic/components/pynnhw/src/hardware/brainscales/range_checker.py", line 75, in checkParameterRanges
        check_parameter_range(key,value,self.parameter_ranges[key])
      File "/home/vogginger/project/symap2ic/components/pynnhw/src/hardware/brainscales/range_checker.py", line 51, in check_parameter_range
        raise ParameterValueOutOfRangeError(name,value,range)
    range_checker.ParameterValueOutOfRangeError: 30.0 is out of the range supported by the hardware( valid range for parameter tau_refrac is: (0.16, 20.0))


Initialization of state variables
`````````````````````````````````

As the hardware runs continuously and cannot be "stopped", state variables for neuron and synapse models can not be initialized.
Calls like the following `initalize(..)` have no effect.

.. code-block:: python

    Neurons = pynn.Population(10, pynn.IF_cond_exp)
    Neurons.initialize('v', -65.0)  # initialize all voltages to -65. mV, has no effect on hardware


Projections / Synapses
``````````````````````

Currently, synaptic ''delays'' are not configurable from PyNN, as adjustable delays are currently not available on the NM-PM-1 hardware. Synaptic delays lie within a range of 1-4 ms when running with a speedup factor of 10.000. The exact value depends on the ongoing activity and on the distance between neurons on the neuromorphic wafer-scale hardware. Hence the values for the delay parameter are ignored for all `Projection` or `connect()` calls.

The API support for `Projection` is currently limited. Synaptic parameters can not be changed after the instantiation of a Projection, neither can the parameters be read back: all the `getX(), randomizeX(), setX()` methods of Projections don't work.


Hardware-Specific specializations
---------------------------------

Current Input
`````````````

Each HICANN offers 4 periodic current sources, that repeatedly plays back a set of 129 current values. They are available via the `pyNN.hardware.hbp_pm.`'''`PeriodicCurrentSource`''', which follows the API of the `CurrentSources` in other pyNN back-ends. The period length can take on a set of values given in `PeriodicCurrentSource.ALLOWED_PERIODS`.
The maximum (and default) period length is `825.6 ms` when running at a speedup of 10.000.
A pyNN `PeriodicCurentSource` can be injected into several neurons, however, a maximum of 4 neurons per HICANN can receive current input.

.. code-block:: python

    import pyNN.hardware.hbp_pm as sim
    sim.setup()
    Neurons = sim.Population(10,sim.IF_cond_exp)

    # current source parameters
    num_values = sim.PeriodicCurrentSource.MEM_SIZE # get number of values, which are periodically replayed
    period = sim.PeriodicCurrentSource.ALLOWED_PERIODS[-1] # get the highest available period

    # fill the value list
    value_list = []
    amplitude = 1.0 # Amplitude of the Step current (in nA) for the first 20% of the period.
    for i in range(num_values):
        if(i<(num_values/5)) :
         value_list.append(amplitude)
        else:
         value_list.append(0)

    # create current source and inject it into one neuron
    CurrentSource = sim.PeriodicCurrentSource(value_list, period)
    CurrentSource.inject_into(Neurons[0])

.. warning:: note that the `PeriodicCurrentSource` is functional for the REAL hardware system, but not for the ESS.*

Hardware Spike Generators
`````````````````````````

Each HICANN offers 8 Background Event Generators (BEG), that can be used to provide spike input to neurons.
They can fire either regularly or pseudo-randomly with a configurable mean rate between 0.5 and 2500 Hz.
Random spike sequences are generated by means of a 16-bit "linear feedback shift register":http://en.wikipedia.org/wiki/Linear_feedback_shift_register, implementing a maximal-length polynomial such
that the sequence is repeated every 65535 clock cycles, which corresponds to 6.56 seconds in the biological domain. (This assumes PLL of 100 MHz)

.. warning:: Note that the hardware spike generators do not generate Poisson spike trains, but only pseudo random spike trains. For details about the statistics see https://gitviz.kip.uni-heidelberg.de/projects/tns/wiki/PoissonSources

A BEG can be used, by mapping a `PyNN.SpikeSourcePoisson` manually onto a `DenMem` (see "`MappingTool`":https://gitviz.kip.uni-heidelberg.de/projects/mappingtool/wiki/Examples#Using-the-hand-placement"), i.e. taking over the slot that usually is used by a real neuron. Hence the number of neuron slots is reduced by one.
Note that there can be only *ONE* `SpikeSourcePoisson` mapped to a block of 64 `DenMems`, that share one priority encoder, i.e. 32 `DenMems` from upper and 32 from lower block each. The block of each `DenMem` is given by ` block = (denmem_id%256) / 32`.

.. code-block:: python

    import pyNN.hardware.hbp_pm as pynn

    # import mapper for handplacement
    from pyNN.hardware.hbp_pm import mapper
    place = mapper.place()

    # call setup, create neurons, etc...

    # Poisson Spike Source Parameters
    poisson_source_params = {
        'start'    : 1000., # start of poisson spike train
        'duration' : 2000., # duration of poisson spike train
        'rate'     : 500.,	# Mean spike frequency(Hz)
        'random':True, # True is default, False for regular spiking of background event generator
        }
    mySpikeSource= pynn.Population(1,pynn.SpikeSourcePoisson,cellparams=poisson_source_params)

    #place a single SpikeSource to a denmem.
    place.to( mySpikeSource[0], hicann=0, neuron=96)

    # commit placement
    place.commit()

    # run experiment, etc.

Note that parameters `duration` and `start` are ignored, if a `SpikeSourcePoisson` is mapped onto a HW Spike Generator.
By setting parameter `random` to `False`, the BEG can be used in regular mode.

Mapping Analyzer
````````````````

Saving the realized and lost connection matrix
''''''''''''''''''''''''''''''''''''''''''''''

The `hardware.brainscales` backend offers a tool to analyse the distortion of the networked mapped onto the hardware.
Therefore, one first tells the mapping to write the lost and realized connections to files.
These files must be specified in `pynn.setup(..)`, otherwise this data is not extracted:

.. code-block:: python

    import pyNN.hardware.hbp_pm as sim

    realized_conn_file = "realized_conns.txt"
    lost_conn_file = "lost_conns.txt"

    sim.setup(
            realizedConnectionMatrixFile = realized_conn_file,
            lostConnectionMatrixFile = lost_conn_file,
              )


The mapping process then generates files containing the realized rsp. lost connection matrix of the network.
The connectivity is saved as a sparse matrix, i.e. for each neuron a list of target neurons is saved::

    <ID1>:<white space separated list of target neurons>
    <ID2>:<white space separated list of target neurons>
    ...

Therefore, the `pyNN.ID` of the cells/neurons is used. In the `pyNN.hardware.hbp_pm` backend, cell IDs are counted as follows:

* Real Neurons get positive integers starting from 0 in the order as they are created.
* Spike Sources get negative integers starting from -1 in the order created.

Hence, the connection matrix file can be read as follows:

::

    -1: 0  # Spike Source -1 has an afferent connection to Neuron 0
    0: 1 2 # Neuron 0 has afferent connections to Neurons 1 and 2


.. warning:: Note that, currently, the mapping process does not support multiple synapses between pairs of neurons. Therefore, it can happen that a target neuron occurs multiple times in the lost-connections files, but only once in the realized matrix.

Analyzing the (distorted) network
'''''''''''''''''''''''''''''''''

The files with the realized and lost connections matrix can be read in by the `MappingAnalyzer`, which is available in the `mapper` module:

.. code-block:: python

    from pyNN.hardware.hbp_pm import mapper

    MA = mapper.MappingAnalyzer(lost_conn_file, realized_conn_file)

Where `lost_conn_file` and `realized_conn_file` are file names of the lost rsp. realized connection matrix of the network.

Example output::

    Mapping Statistiscs:
    19881  of  61881  Synapses lost ( 32.1277936685 %)


The `MappingAnalyzer` holds the lost and realized sparse connection matrices between cells.
It offers several methods to e.g. get the number of lost and realized connections between groups of source and target neurons.
One can also directly print the synapse loss between the groups.

Full Example
````````````

For an example making use of the full functionality of the `MappingAnalyzer`, see here:
https://gitviz.kip.uni-heidelberg.de/projects/mappingtool/repository/revisions/master/entry/misc/tests/examples/mapping_analyzer/main.py


Customizing your Hardware Experiment
------------------------------------

With the pyNN `setup` options you can customize your hardware experiment.

Boosting Synaptic Weights
`````````````````````````

TODO

Multiple Runs
`````````````

The pyNN hardware backend allows multiple calls of `run(..)`.
The only variables you can change after `run()` has been called once are the following:

* The input spiketrains of spike sources

What can **not** be done after the first run is the following:

* create new neurons
* draw new connections
* change synapse or neuron parameters
* change the recording information

After each run, you need to call 'reset()' to set back the simulation time to 0 and clear the recorded data.
It is not possible to call 'run(..)' several times without calling 'reset()' in between.
This is different to software simulators, where the simulation time is accumulated and the states (membrane potential etc.) are preserved for the next run.
In contrast, on the hardware, the analog states can not be preserved, so that multiple runs without reset in between make no sense.
Calling `getSpikes()` or `printSpikes(..)` considers only the spikes from the latest run.

.. note:: for multiple runs there is an option to program floating gates only once: just set `pyNN.setup(programFloatingGates="once")` (this is the default).

**Example:**

For a full example see https://gitviz.kip.uni-heidelberg.de/projects/mappingtool/repository/entry/misc/tests/examples/single_neuron_l2_input/single_neuron_l2_input_multiple_runs.py
where this the I-O Frequency Curve of a neuron is measured with this option.


Speedup Factor
``````````````

You can specify the speedup factor, which determines how much faster the emulation on the hardware takes place compared to biological real time:

.. code-block:: python

    pyNN.setup(speedupFactor=10000)

The default is 10000. When the speedup is changed, the neuron and synapse parameter ranges are automatically adapted.


Using the Small Capacitance
```````````````````````````

For the hardware neuron one has the choice from two different capacitors used as the membrane capacitance.
Per default the big capacitor with 2.6 pF is used.
By setting

.. code-block:: python

    pyNN.setup(useSmallCap=True)

one can switch to the small capacitance with 0.4 pF.
Then, the parameter ranges of the membrane time constant `tau_m`, the adaption variables `a` and `b` as well as synaptic weights are updated.
This option is useful when running at a high speedup factor (e.g. 20000).

.. warning:: note that there is currently no calibration data available for the small capacitance, such that hardware experiments are not expected to use a precise transformation of neuron parameters to the hardware.''

Ignoring Hardware Parameter Ranges
``````````````````````````````````

One can disable the check if the biological parameters fit to those on the hardware by setting:

.. code-block:: python

    pyNN.setup(ignoreHWParameterRanges=True)

This is option is useful for ESS simulations or when only the mapping is analyzed.
For hardware experiment this option is not recommended!

Synapse and Neuron Loss
```````````````````````

On the hardware the resources for neurons and synapses are limited. The number of available hardware neurons and synapses depends on the chosen hardware setup and the hardware neuron size, see below. Furthermore, it can happen that some synapses from the PyNN model can not be realized on the hardware, as they are ''lost'' during the mapping process. The reason for that can be limited configurability of the hardware circuits, or non-optimal algorithms for the very-complex mapping process. More details on the sources of synapse loss and compensation techniques can be found in [http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0108590 Petrovici et al. 2014].

The user can specify the maximum allowed neuron and synapse loss for a given network with the following `pynn.setup` parameters::

    maxSynapseLoss - maximum synapse loss allowed during mapping.
                     default: 0.0
                     range: (0.0, 1.0)
    maxNeuronLoss  - maximum neuron loss allowed during mapping.
                     default: 0.0
                     range: (0.0, 1.0)

Here, synapse/neuron loss refers to the fraction of synapses/neurons, that can not be mapped onto the hardware.
By specifying this limit, the user can avoid experiments where the too many synapses or neurons are lost. Per default, the mapping stops if any neuron or synapse can not be mappped.

ESS specifics
-------------

`pyNN.setup` options
````````````````````

There are several options in pyNN.setup() which only have an effect when the ESS is used.
In order to use the ESS parameter `useSystemSim` has to be set to `True`.
Other parameters::

    `param useSystemSim - specifies if the executable system simulation, i.e. a virtual hardware, shall be
                          used instead of a real hardware system.
    `param ess_params   - dictionary containing parameters, that are only considered when using the ESS (useSystemSim=True):
                          parameters:
                             `param perfectSynapseTrafo - Use a perfect synapse transformation, instead of the only available ideal synapse trafo. boolean
                             `param weightDistortion    - specifies the distortion of synaptic weights in the virtual hardware system.
                                                          This parameters define the fraction of the original value, that is used as
                                                          the standard deviation for randomizing the weight according to a normal(Gaussian)
                                                          distribution around the original value.
                             `param pulseStatisticsFile - name of file, to which the ESS pulse statistics are written
    `param hardware     - a list of hardware setups to be used.
                             Each setup is specified by a dictionary with the following parameters:
                                 setup           - specifies the type of the hardware
                                                   default: wafer
                                                   choices: ['vertical_setup', 'wafer']
                                 wafer_id        - the logical id of the wafer in the Calibration Database
                                                   default: 0
                                 hicannIndices   - a list of HICANN Indices (HALBE Enumeration) that shall be used for mapping.
                                                   If not specified, all HICANNs of the wafer will be used.
                                                   default: range(384)
                                 setup_params    - dictionary specifying the parameters of the hardware setup
                                                   params:
                                                       ip            - IP Address (v4) of FPGA of vertical setup as string in dotted decimal form.
                                                                       Only used if setup is a 'vertical_setup'
                                                                       default: 192.168.1.1
                                                       num_hicanns   - number of HICANNs in the JTAG chain of vertical setup
                                                                       default: 1
                                                                       range: (1, 8)
                          default: [{'setup': 'wafer', 'wafer_id': 0, 'hicannIndices':range(384)}]
    `param hardwareNeuronSize - specifies the size of hardware neurons, i.e. the number of neuron circuits that are used to form a larger neuron.
                                The higher this number, the higher is the number of incoming synapses per neuron, and the lower is the total
                                number of neurons
                                default: 1
                                choices: [1, 2, 4, 8, 16, 32, 64]


There are several predefined hardware setups for the use with the ESS in the dictionary `pyNN.hardware.hbp_pm.hardwareSetup`, see below for details.
E.g. the following sets up the ESS with a hardware consisting of one reticle, using 1 `DenMem` per neuron, with a fixed pattern noise of 20 % of the synaptic weights, and a perfect synapse transformation:

.. code-block:: python

    pynn.setup(useSystemSim=True,
               hardware=pynn.hardware["one-reticle"],
               hardwareNeuronSize=1,
               ess_params={
                    'perfectSynapseTrafo': True,
                    'weightDistortion': 0.2}
               )


How to change the number of neurons per HICANN
``````````````````````````````````````````````

Each HICANN has 512 neuron circuits (`DenMems`) implementing the `AdEx` neuron model, and each `DenMem` has 224 incoming synapses. One can combine several `DenMems` to build larger neurons with more incoming synapses, of course, this reduces the overall number of neurons.

The number of hardware neurons (`DenMems`) per neuron, and thus the number of neurons per HICANN, can be controlled via the setup parameter `hardwareNeuronSize`.

.. code-block:: python

    pynn.setup(hardwareNeuronSize=1)

The following table shows how the parameter `hardwareNeuronSize` controls the effective number of neurons per HICANN  and the number of incoming synapses per neuron:

====================  ================  =================
`hardwareNeuronSize`  `Neurons/HICANN`  `Synapses/Neuron`
====================  ================  =================
1                     472               224
2                     236               448
4                     118               896
8                     59                1792
16                    32                3584
32                    16                7168
64                    8                 14336
====================  ================  =================

By default a hardware neuron size of 1 is used.

.. note:: Why is the effective number of neurons smaller than 512 divided by `hardwareNeuronSize` for values up to 8?

          This is due to a technical limitation: Up to 64 neuron inject their pulses into a on-wafer routing bus. Each neuron then has a neuron address between 0-63 on that bus. Address 0 can not be used by normal neurons, as it is required for a background event generator, which continuously sends pulses over the routing buses in order to keep asynchronous buses "locked". When a pulse with the given 6-bit address enters a synapse array, for each synapse it is checked whether the pulse address matches a configured address per synapse. As there is no extra bit to disable a hardware synapse, this has to be done with the address: The synapse has to be configured with an address that never arrives. For each block of 16 addresses ( [0-15], [16-31], [32-47], [48-63] ), one address needs to be reserved for disabling the synapse.
          Hence there are only 59 Addresses per bus that can be used per routing bus.

Available hardware setups
`````````````````````````

As mentionend  above, one can choose from different predefined hardware setups via:

.. code-block:: python

    import pyNN.hardware.hbp_pm as pynn
    pynn.setup( useSystemSim=True,
                hardware = pynn.hardwareSetup[<SETUP>]
              )

Here are the details about the different hardware setups:

===============  ==========  ========
`hardwareSetup`  `#HICANNs`  geometry
===============  ==========  ========
'one-hicann'     1
'one-reticle'    8           4x2
'small'          32          8x4
'medium'         128         16x8
'medium2'        128         32x4
'large'          240         20x12
'large2'         224         28x8
'one-wafer'      384         `WaferMap <http://129.206.127.67/jss/WaferMapShow?scale=1.0&theta=1.5709999799728394&waferNumber=1&drawMode=DRAW_MODE_HICANN_ConfigID>`_
===============  ==========  ========

Per default a complete wafer('one-wafer') is used. It is strongly recommended to choose a smaller hardware setup for ESS runs to reduce the simulation time.

The following table shows the **total number of neurons** depending on the `hardwareNeuronSize` and the `hardwareSetup`

===============  ======  =====  =====  =====  =====  ====  ====
`hardwareSetup`            `hardwareNeuronSize`
---------------  ----------------------------------------------
\                1       2      4      8      16     32    64
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
''''''''''''''''''''''

The bandwidth for external simulus spikes (from `SpikeSourcePoisson` and `SpikeSourceArray`) is limited on the hardware.
The following table lists the maximum input bandwidth **for a speedup factor of 10000**:

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

Perfect Synapse Transformation
``````````````````````````````

Currently, there exists only one set of calibration data for the transformation of synaptic weights to the hardware.
I.e., there is only one configuration of the synapse drivers, for which a calibration has been done in ideal transistor-level hardware simulations, such that one is restricted to exactly 16 different synaptic weight settings in the hardware.

But, in principle, one can use different settings for the synapse drivers to allow a wider range of synaptic weights. This will be available in the near future.

In order to already mimic this behavior with the ESS, one can choose the ''perfect synapse transformation'', which generates different configurations of the synapse driver such that the associated synaptic weights match those specified in PyNN, at least within the the 4-bit resolution of the digital weights.

.. code-block:: python

    pynn.setup( useSystemSim=True, ess_params = {'perfectSynapseTrafo':True})


Pulse Loss Statistics
`````````````````````

The ESS allows to count all spikes that were lost in any place of the virtual hardware system.
Spikes are mostly lost in the off-wafer communication network (also called ''Layer 2 network'') that connects the wafer to the host PC.
In the Layer 2 network pulse loss can happen on two routes:

1. Stimulation:
   not all spikes from the spike sources (`SpikeSourcePoisson` or `SpikeSourceArray`) are delivered to its targets, because the bandwidth in the off-wafer network is limited. When a spike is lost, it is lost for its targets.

2. Recording:
   For the same bandwidth constraints in the off-wafer network, some spikes of real neurons can be lost on the route from the wafer to the FGPGAs, Hence, in the received spike data some events are missing.
   However, the ''non-recorded'' spikes did reach their target neurons on the wafer.

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


You can specify to get this data by specifying a file `pulseStatisticsFile` in the setup command:

.. code-block:: python

    pynn.setup(useSystemSim=True, ess_params={'pulseStatisticsFile': 'pulse_stats.py'})


Then the pulse statistics file contains a Python dictionary `pulse_statistics` which can be use for further processing:

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



NM-MC-1 system
==============

stuff specific to the pyNN.spinnaker backend


.. _PyNN: http://neuralensemble.org/PyNN/
.. _`PyNN 0.7 documentation`: http://neuralensemble.org/trac/PyNN/
.. _`PyNN 0.8 documentation`: http://neuralensemble.org/docs/PyNN/
