==========================
Using the SpiNNaker system
==========================

As explained in :ref:`building_models`, both the experiment description and the model description
for the SpiNNaker system must be written as Python scripts,
using the PyNN application programming interface (API).
The implementation of the PyNN for the SpiNNaker system is called :py:mod:`sPyNNaker`, and
is also available as the module :py:mod:`pyNN.spiNNaker`:


.. code-block:: python

    import pyNN.spiNNaker as sim

sPyNNaker implements a subset of the PyNN API.  See the `external 'sPyNNaker Models, Limitations and Extensions' <https://spinnakermanchester.github.io/latest/spynnaker_limitations.html>`_ for details of the features supported. 


Mapping and Routing
===================

The mapping process examines the neural network definition and attempts to break it down in to parts, each of which can be executed on a SpiNNaker core.  A routing algorithm is then run to work out the communication paths between the cores on the SpiNNaker network.  In the current software, mapping and routing takes place on the host machine as part of the placement and configuration manager (PACMAN).

It is possible for end users to add their own mapping and routing algorithms into the tool chain.  Instructions on how to do so can be found `here <http://spinnakermanchester.github.io/latest/mapping_algorithms.html>`__.
