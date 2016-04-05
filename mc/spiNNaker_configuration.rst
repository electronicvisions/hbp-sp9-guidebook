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
executes this application on the MC-1 hardware and supports the retrieval of
application data generated during the applications execution.

The different versions of the high level software can be found below:
2015.005 “Arbitrary” `sPyNNaker front end Arbitrary`_
2016.001 “Another Fine Product.." `sPyNNaker front end Another`_


Supported cells and plasticity mechanisms
=========================================

 The MC-1 PyNN module within the software stack (named sPyNNaker for clarity
 sakes) currently supports a subset of the standard PyNN 0.75 interface. The
 supported interface functions can be found in the online documentation under

 2015.005 “Arbitrary”
 `Configuring the sPyNNaker front end, and its limitations`_

 2016.001 “Another Fine Product.."
 `PyNN on SpiNNaker Support and Limitations`_

 In the next planned release, 2016.002 “Inspiral, Coalescence, Ringdown”,
 there is plans to have all of PyNN 0.75 supported and started PyNN 0.8 support.

Parameter ranges
================

All parameters and their ranges are under software control. Currently, in 
versions 2015.005 “Arbitrary” and 2016.001 “Another Fine Product..", weights are
held as 16-bit integers, with their range determined at compile-time to suit
the application. Membrane voltages are held as 32-bit fixed point numbers in
the s16.15 format, representing mV.

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
 :class:`Projection` class are loaded onto the machine during the execution of
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
 sPyNNakerExternalDevicesPlugin

A description on how to use this functionality can be found on the online
documentation for the different versions of tools below:
2015.005 “Arbitrary”
_`Simple Input/output and Visualisation using sPyNNaker`_

2016.001 “Another Fine Product.."
_`Instructions on using the SpyNNaker External Device Plugin for closed loop simulations`_

Projections
===========

The MC-1 software stack supports projections as part of the model's software
that runs on the hardware. Therefore we synaptic delays as programmable aspects.

There is a limit on how much delay can be added to a model's synapse.

Currently, in both version 2015.005 “Arbitrary” and 2016.001
“Another Fine Product..", we are restricted to representing delays
as 0-31 timer ticks. Each timer tick — which can be set under software 
control — is usually set to be 0.1ms or 1ms, but this is just a choice made 
by the programmer. Longer delays are implemented using a dummy population 
of so-called “delay neurons”; these are added by the configuration software
if needed and support the user up to 144 timer ticks.

The next planned release, 2016.002 “Inspiral, Coalescence, Ringdown”, will
remove this restriction giving an unlimited number of directly represented
timer ticks for each delay.

Synapse and neuron loss
=======================

The MC-1 software stack removes projection links between two collections of
neurons that were initially defined as connected if the connectivity between
the two sets is determined to be zero when the projection is realised in
the software's mapping process.

Because the MC-1 communication fabric is lossy, there is the chance that during
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
 documentation for version 2016.001 “Another Fine Product.." under
  `Instructions on using the sPyNNaker reload functionality`_

Available hardware setups
=========================

There are currently four known hardware setups:

The 600 48 node board machine, a 48 node board; the four-node board and Jorg Conradt’s one-node board.
The first one provides the machine that support the HBP portal, the next two
were produced at The University of Manchester, the third is
produced at TU Munchen and is intended for light-weight near-robotic 
applications.

When using the HBP portal, allocation of the machine is done on a PyNN script
basis and allocates either a single 48 chip board or a machine which consists
of sets of 3 48 chip boards, referred to as triad. This logic is done
automatically when using the portal by first measuring the size of the
 network to be simulated and allocating accordingly.

Both versions 2015.005 “Arbitrary” and 2016.001 “Another Fine Product.."
support the ability to be turned into virtual mode, where the tools execute
the PyNN script as if it was linked to a direct SpiNNaker machine, but
without actually generating any simulated data. This supports end users in
testing their scripts before loading them into the HBP portal for basic
compilation errors. Instructions on how to use this functionality can be
found under 2016.001 “Another Fine Product.."
 `Instructions on how to use the different front ends in virtual mode`_

Mapping
=======

In both version 2015.005 “Arbitrary” and 2016.001 “Another Fine Product.." the mapping and routing process takes place
on the host machine as part of the placement and configuration manager 
(PACMAN). In the next planned release, 2016.002 “Inspiral, Coalescence, Ringdown”,
we migrate this process on to the SpiNNaker hardware itself. The expectation 
is that this will significantly improve load-times.

In version 2016.001 “Another Fine Product.." there is a interface for end users
to add their own mapping and routing algorithms into the tool chain.
Instructions on how to do so can be found under
 `Using new mapping algorithms with different front ends`_



.. _`SpiNNaker hardware`: http://apt.cs.manchester.ac.uk/projects/SpiNNaker/
.. _SARK: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/sark.pdf
.. _Spin1API: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/spinn_api_doc.pdf
.. _Ybug: https://github.com/SpiNNakerManchester/spinnaker_tools/tree/2015.002/docs/ybug.pdf
.. _`sPyNNaker front end Arbitrary`: https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005
.. _`sPyNNaker front end Another`: https://github.com/SpiNNakerManchester/sPyNNaker/tree/2016.001
.. _`Configuring the sPyNNaker front end, and its limitations`: http://spinnakermanchester.github.io/2015.005.Arbitrary/
.. _`Simple Input/output and Visualisation using sPyNNaker`:http://spinnakermanchester.github.io/2015.005.Arbitrary/
.. _`Instructions on using the SpyNNaker External Device Plugin for closed loop simulations`:http://spinnakermanchester.github.io/2016.001.AnotherFineProductFromTheNonsenseFactory/spynnaker_index.html
.. _`2.6 Rerunning PyNN scripts`: https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/wiki/2015.004:-Little-Rascal-:-2.5-Rerunning-PyNN-scripts
.. _`Instructions on using the sPyNNaker reload functionality`: http://spinnakermanchester.github.io/2016.001.AnotherFineProductFromTheNonsenseFactory/spynnaker_index.html
.. _`Using new mapping algorithms with different front ends`: http://spinnakermanchester.github.io/2016.001.AnotherFineProductFromTheNonsenseFactory/spynnaker_index.html
.. _`Instructions on how to use the different front ends in virtual mode`: http://spinnakermanchester.github.io/2016.001.AnotherFineProductFromTheNonsenseFactory/spynnaker_index.html
.. _`PyNN on SpiNNaker Support and Limitations`: http://spinnakermanchester.github.io/2016.001.AnotherFineProductFromTheNonsenseFactory/spynnaker_index.html