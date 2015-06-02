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

    In (a) Microphotograph of the Spikey neuromorphic chip.
    In (b) Photograph of the Spikey neuromorphic system.
    The Spikey chip is covered by a black seal.
    Adapted from [Pfeil2013]_.

The Spikey chip is fabricated in a 180nm CMOS process with die size :math:`5\,mm \times 5\,mm`.
While the communication to the host computer is mostly established by digital circuits, the spiking neural network is mostly implemented with analog circuits.
Compared to biological real-time networks on Spikey chips are accelerated, because time constants on the chip are approximately :math:`10^4` times smaller than in biology.
Each neuron and synapse has its physical implementation on the chip.
The total number of 384 neurons are split into two blocks of 192 neurons with 256 synapses each.
Each line of synapses in these blocks, i.e. 192 synapses, is driven by a *synapse line driver* that can be configured to receive input from either external spike sources (e.g., generated on the host computer) or from on-chip neurons.

.. figure:: spikey_topology.png
    :align: center
    :alt: Network topology
    :width: 400px

    Connection scheme for on-chip neurons:
    Synapse drivers (red) can be configured to receive either input from the same or the other block of neurons (blue).
    For each synapse (green) its weight can be configured with a 4-bit resolution, i.e., 16 different values.

.. todo:: add info about neuron
.. todo:: add info about synapse driver
.. todo:: add info about synapse
.. todo:: add info about stp
.. todo:: add info about stdp

.. todo:: quick intro to programming
.. todo:: quick intro to PyNN
.. todo:: quick intro to hardware
.. todo:: quick intro to config space

Lesson 1: Exploring the parameter space
---------------------------------------

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
