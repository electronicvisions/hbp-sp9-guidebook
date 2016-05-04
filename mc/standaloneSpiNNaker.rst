===============================
The SpiNNaker standalone system
===============================

SpiNNaker boards and multi-board systems can be used directly connected to your laptop or PC.  This requires the installation of the software stack on your host machine to control the board.

Installation and use of the SpiNNaker software
==============================================

Instructions on how to install the most recent SpiNNaker high level software stack can be found `here <http://spinnakermanchester.github.io/latest/spynnaker_install.html>`__.

There is a tutorial on creating basic PyNN networks and running them on SpiNNaker `here <http://spinnakermanchester.github.io/latest/spynnaker_tutorial.html>`__, and another tutorial on using STDP plasticity on SpiNNaker `here <http://spinnakermanchester.github.io/latest/spynnaker_plasticity_tutorial.html>`__.

Extending the SpiNNaker Software
================================

The software that executes on the SpiNNaker machine is written in C code, so it is not too difficult to extend this to run new neural, synapse and plasticity models, amongst other things.  Instructions on how to extend the software can be found `here <http://spinnakermanchester.github.io/latest/spynnaker_new_models.html>`__.

Generating Live Input and Output
================================

SpiNNaker extends PyNN by allowing live input and output from the simulation during execution.  This can be used for communication with external devices or other simulations, such as robotic devices or robotic simulations, or for visualisation during the simulation.  Instructions on the use of this feature can be found `here <http://spinnakermanchester.github.io/latest/spynnaker_external_io.html>`__.
