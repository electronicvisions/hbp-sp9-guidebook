================================
The SpiNNaker "many core" system
================================

The MC-1 machine is designed to utilise the power of digital hardware and
support various models/application though the use of programmable software that
can run on ARM cores. A description of the hardware can be located online at

`SpiNNaker hardware`_

The MC-1 has a amount of software support to allow the PyNN interface to execute
on the MC-1 machine, These range from low level software:

 SARK_: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/sark.pdf
 Spin1API_: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/spinn_api_doc.pdf
 Ybug_: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/ybug.pdf

to high level software that takes a graph representation of an application (in
this case a PyNN description of a Neural network) and maps, optimises and
executes this application on the MC-1 hardware and supports the retrival of
application data generated during the applications execution.

`sPyNNaker front end`_


Supported cells and plasticity mechanisms
=========================================

 The MC-1 PyNN module within the software stack (named sPyNNaker for clarity
 sakes) currently supports a subset of the standard PyNN interface. The
 supported interface functions can be found in the online documentation under
 `Configuring the sPyNNaker front end, and its limitations: Limitations`_

Parameter ranges
================

 TODO Not sure if this section is really needed for our stuff.

Recording spikes, membrane potential and synaptic conductance
=============================================================

 The spikes of all neurons mapped onto the hardware as well as the input spikes
 can be recorded. Spikes are returned to the PyNN script via the standard PyNN
 interface (i.e., the :func:`getSpikes()` and :func:`printSpikes()` methods of
 the :class:`Population` class)

 The membrane potential of all neurons mapped onto the hardware can be recorded.
 Membrane potential's are returned to the PyNN script via the standard PyNN
 interface (i.e., the :func:`getV()` and :func:`printV()` methods of the
 :class:`Population` class)

 The Synaptic Conductance of all neurons mapped onto the hardware can be
 recorded. Synaptic Conductance's are returned to the PyNN script via the
 standard PyNN interface (i.e., the :func:`get_gsyn()` and :func:`print_gsyn()`
 methods of the :class:`Population` class)

Initialisation of state variables
=================================

 As the models in the MC-1 hardware are represented by software models, the
 state variables defined on the :class:`Population` class and
 :class:`Projection` class are loaded onto the machine during the exeuction of
 the standard PyNN interface :func:`run()`. This is also the function which
 executes the model on the hardware.

Injected current
================

 The MC-1 software stack currently supports two standard ways to inject
 current into a PyNN simulation executing on the hardware. These are the
 :class:`SpikeSourceArray` class and the :class:`SpikeSourcePoisson` class.

 A third, none standard PyNN interface, way of injecting current into a
 PyNN simulation executing on the hardware is through live injection from a
 external device. These functions are supported by our
 sPyNNakerExternalDevicesPlugin_

A description on how to use this functionality can be found on the online
documentation under _`2.1 Injecting Data Into SpiNNaker Machines`:

Projections
===========

The MC-1 software stack supports projections as part of the model's software
that runs on the hardware. Therefore we synaptic delays as programmable aspects.

There is a limit on how much delay can be added to a model's synapse.

TODO: chase up what this limit is

Synapse and neuron loss
=======================

The MC-1 software stack removes projection links between two collections of
neurons that were initially defined as connected if the connecitvity between
the two sets is determined to be zero when the projection is relaised in
the software's mapping process.

Becuase the MC-1 communciation fabric is lossy, there is the chance that during
execution packets that were transmitted from one core may not reach its
destination.

Changing the number of incoming synapses per neuron
===================================================

The MC-1 software stack supports projections as part of the model's software
that runs on the hardware. Therefore the number of incoming synapses supported
per neuron is limited by the resources used to store the synapses, or in the
limitation of the hardware on the peak throughput to a core (known at six
million spikes per second) in terms of routed packets.

Multiple runs
=============

 The MC-1 software supports multiple runs of the same PyNN script, a
 description of how to rerun a PyNN script can be found in the online
 documentation under `2.6 Rerunning PyNN scripts`_

Available hardware setups
=========================

TODO Dont know what to put here

Mapping
=======

TODO Dont know if we should delve into the software stacks mapping processes.

.. _`SpiNNaker hardware`: http://apt.cs.manchester.ac.uk/projects/SpiNNaker/
.. _SARK: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/sark.pdf
.. _Spin1API: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/spinn_api_doc.pdf
.. _Ybug: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/ybug.pdf
.. _`sPyNNaker front end`: https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.004
.. _`Configuring the sPyNNaker front end, and its limitations: Limitations`: https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/wiki/2015.004:-Little-Rascal-:-1.1-Configuring-the-sPyNNaker-front-end,-and-its-limitations
.. _sPyNNakerExternalDevicesPlugin:  https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.008
.. _`2.6 Rerunning PyNN scripts`: https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/wiki/2015.004:-Little-Rascal-:-2.5-Rerunning-PyNN-scripts
