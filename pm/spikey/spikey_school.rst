Spikey school
=============

Introduction
------------

For an introduction to the Spikey neuromorphic system, its topology and configuration space, see section 2 in [Pfeil2013]_.
Detailed information about the implementation of the neuron, STP and STDP models are given in Figure 17 in [Indiveri2011]_, [Schemmel2007]_ and [Schemmel2006]_, respectively.
The following paragraph will briefly summarize the features of the Spikey system.

.. figure:: spikey_system.png
    :align: center
    :alt: The Spikey system
    :width: 400px

    A photograph of the Spikey neuromorphic chip (a) and system (b), respectively.
    In (b) the Spikey chip is covered by a black seal.
    Adapted from [Pfeil2013]_.

The Spikey chip is fabricated in a 180nm CMOS process with die size :math:`5\,mm \times 5\,mm`.
While the communication to the host computer is mostly established by digital circuits, the spiking neural network is mostly implemented with analog circuits.
Compared to biological real-time, networks on the Spikey chip are accelerated, because time constants on the chip are approximately :math:`10^4` times smaller than in biology.
Each neuron and synapse has its physical implementation on the chip.
The total number of 384 neurons are split into two blocks of 192 neurons with 256 synapses each.
Each line of synapses in these blocks, i.e. 192 synapses, is driven by a *line driver*
that can be configured to receive input from external spike sources (e.g., generated on the host computer), from on-chip neurons in the same block or from on-chip neurons in the adjacent block.

.. todo:: mention 4th input?

.. figure:: spikey_topology.png
    :align: center
    :alt: Network topology
    :width: 400px

    Numbering of neurons (blue) and line drivers (red).
    Here, only connections within the same block of neurons are shown.
    For connections between the blocks see the following table.
    The weight of each synapse (green) can be configured with a 4-bit resolution, i.e., 16 different values.

.. TP: table directive does not work
Neuron assignment to line drivers.
The last (upper) 64 line drivers receive external inputs only and hence external spike sources line drivers are allocated from top to bottom.

==============  ====================  ===================== ==============  ====================  =====================
Line driver ID  Neuron ID left block  Neuron ID right block Line driver ID  Neuron ID left block  Neuron ID right block
==============  ====================  ===================== ==============  ====================  =====================
0               0                     193                    256             192                    1
1               1                     192                    257             193                    0
2               2                     195                    258             194                    3
3               3                     194                    259             195                    2
...             ...                   ...                    ...             ...                   ...
190             190                   383                    446             382                   191
191             191                   382                    447             383                   190
192             ext only              ext                    448             ext only              ext only only
...             ...                   ...                    ...             ...                   ...
255             ext only              ext                    511             ext only              ext only only
==============  ====================  ===================== ==============  ====================  =====================

The hardware implementations of neurons and synapses are inspired by the leaky integrate-and-fire neuron model using synapses with exponentially decaying or alpha-shaped conductances.
While the leak conductance and (absolute) refractory period is individually configurable for each neuron,
the resting, reset, threshold, excitatory reversal and inhibitory reversal potentials are shared among neurons (see [Pfeil2013]_ for details).
Line drivers generate the time course of postsynaptic conductances (PSCs) for a single row of synapses.
Among other parameters the rise time, fall time and amplitude of PSCs can be modulated for each line driver.
Each synapse stores a configurable 4-bit weight.
A synapse can be turned off, if its weight is set to zero.

.. todo:: list parameter names
.. todo:: add sketch for PSC

.. todo:: add info about stp
.. todo:: add info about stdp

.. todo:: quick intro to programming
.. todo:: quick intro to PyNN
.. todo:: quick intro to hardware
.. todo:: quick intro to config space

Lesson 1: Exploring the parameter space
---------------------------------------

.. figure:: rate_over_gleak.png
    :align: center
    :alt: Rate over leak conductance
    :width: 400px

    Average firing rate in dependence on leak conductance :math:`g_{leak}` (`source code <https://github.com/electronicvisions/spikey_demo/blob/master/networks/rate_over_gleak.py>`_).

Lesson 2: Feedforward networks
------------------------------

Lesson 3: Recurrent networks
----------------------------

Lesson 4: Short-term plasticity
-------------------------------

Lesson 5: Long-term plasticity
------------------------------

Lesson 6: Something functional
------------------------------

.. [Pfeil2013] Pfeil et al. (2013). `Six networks on a universal neuromorphic computing substrate <http://arxiv.org/pdf/1210.7083>`_. Front. Neurosci. 7 (11).
.. [Indiveri2011] Indiveri et al. (2011). `Neuromorphic silicon neuron circuits <http://journal.frontiersin.org/article/10.3389/fnins.2011.00073/pdf>`_. Front. Neurosci. 5 (73).
.. [Schemmel2007] Schemmel et al. (2007). `Modeling synaptic plasticity within networks of highly accelerated I&F neurons <http://www.kip.uni-heidelberg.de/Veroeffentlichungen/download.php/4799/ps/schemmel_iscas2007_spikey.pdf>`_. In Proceedings of the 2007 International Symposium on Circuits and Systems (ISCAS), New Orleans, pp. 3367–3370. IEEE Press.
.. [Schemmel2006] Schemmel et al. (2006). `Implementing synaptic plasticity in a VLSI spiking neural network model <http://www.kip.uni-heidelberg.de/Veroeffentlichungen/download.php/4620/ps/1774.pdf>`_. In Proceedings of the 2006 International Joint Conference on Neural Networks (IJCNN), Vancouver, pp. 1–6. IEEE Press.
