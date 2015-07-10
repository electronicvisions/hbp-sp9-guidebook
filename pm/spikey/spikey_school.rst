Spikey school
=============

.. _label-intro:

Introduction
------------

For an introduction to the Spikey neuromorphic system, its topology and configuration space, see section 2 in [Pfeil2013]_.
Detailed information about the analog implementation of the neuron, STP and STDP models are given in Figure 17 in [Indiveri2011]_, [Schemmel2007]_ and [Schemmel2006]_, respectively.
The digital parts of the chip architecture are thoroughly documented in [Gruebl2007]_.
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

The hardware implementations of neurons and synapses are inspired by the leaky integrate-and-fire neuron model using synapses with exponentially decaying or alpha-shaped conductances (PyNN neuron model ``IF_facets_hardware1``).
While the leak conductance (PyNN neuron model parameter ``g_leak``) and (absolute) refractory period (``tau_refrac``) is individually configurable for each neuron,
the resting (``v_rest``), reset (``v_reset``), threshold (``v_thresh``), excitatory reversal (clamped to ground) and inhibitory reversal potentials (``e_rev_I``) are shared among neurons (see [Pfeil2013]_ for details).
Line drivers generate the time course of postsynaptic conductances (PSCs) for a single row of synapses.
Among other parameters the rise time, fall time and amplitude of PSCs can be modulated for each line driver (for details see :ref:`lesson_1` and Figure 4.8 and 4.9 in [Petkov2012]_).
Each synapse stores a configurable 4-bit weight.
A synapse can be turned off, if its weight is set to zero.

Network models for the Spikey hardware are described and controlled by PyNN (version 0.6; for an introduction to PyNN see :ref:`building_models`).
Due to the fact that PyNN is a Python package we recommend to have a look at a `Python tutorial <https://docs.python.org/2/tutorial/>`_.
For efficient data analysis and visualization with Python see tutorials for `Numpy <http://wiki.scipy.org/Tentative_NumPy_Tutorial>`_,
`Matplotlib <http://matplotlib.org/users/pyplot_tutorial.html>`_ and `Scipy <http://docs.scipy.org/doc/scipy/reference/tutorial/>`_.

.. todo:: add info about stp
.. todo:: add info about stdp

.. todo:: mention 4th input?
.. todo:: add Bruederle's diss and other publications about chip?

.. _lesson_1:

Lesson 1: Exploring the parameter space
---------------------------------------

.. todo:: add some general words about variation, reproducibility and parametrization

In this lesson we explore the parameter space of neurons and synapses on the Spikey chip.
Due to imperfections in the production process, parameters of neurons and synapses vary across the chip (fixed-pattern noise).
In contrast to these static variations, temporal noise causes different results in consecutive emulations of identical networks.

First, we measure the dependency of the population firing rate on the leak conductance of neurons.
The network comprises ``noNeurons`` neurons, of which each is stimulated by ``noInputs`` inputs randomly drawn from a shared pool of ``noStims`` spike sources.
For each spike source independently, spikes are drawn from a Poisson process with rate ``rateStim``.

.. figure:: schematic_rate_over_gleak.png
    :align: center
    :alt: Schematic - Rate over leak conductance
    :height: 175px

    One random realization of a network with ``noStims=noNeurons=3`` and ``noInputs=2``.
    Synapses with weight zero are not drawn.
    Spike times of all neurons are recorded.

.. figure:: rate_over_gleak.png
    :align: center
    :alt: Rate over leak conductance
    :width: 400px

    Average firing rate in dependence on leak conductance :math:`g_{leak}` (`source code <https://github.com/electronicvisions/spikey_demo/blob/master/networks/rate_over_gleak.py>`_).

**Tasks:**

* Investigate the variability of firing rates across neurons:
  Plot the firing rates of several different single neurons over the leak conductance.
  Quantify the variations of population firing rates by calculating and plotting the errors of the average firing rates.
  Also consider the underlying distribution of firing rates for the default value of the leak conductance.
  Interpret this distribution qualitatively and quantitatively.

* Measure and plot the dependency of the population firing rate on other neuron parameters (see :ref:`label-intro`).
  Interpret these dependencies qualitatively?

* Estimate the ratio between fixed-pattern and temporal noise:
  Measure the reproducibility of emulations, i.e., the error of the average firing rate across identical consecutive trials, using the default neuron parameters for single neurons and populations of neurons.
  Compare this reproducibility to the results of the first task and plot its dependency on both the duration of emulations and the number of consecutive trials.

* Calibrate the firing rates of single neurons to a reasonable target rate by adjusting the leak conductances.

Second, we investigate synaptic parameters by stimulating a single neuron with a single spike and recording its membrane potential.
In order to average out noise on the membrane potential (mostly caused by the readout process) we stimulate the neuron with a regular spike train and calculate the spike-triggered average of these so-called excitatory postsynaptic potentials (EPSPs).

.. figure:: schematic_epsp.png
    :align: center
    :alt: Schematic - EPSPs on hardware
    :height: 175px

    A single neuron is stimulated by using a single synapse.
    The parameters of synapses are adjusted row-wise in the line drivers.
    The membrane potential of the stimulated neuron is recorded.

.. figure:: epsp.png
    :align: center
    :alt: EPSPs on hardware
    :width: 400px

    Single and averaged excitatory postsynaptic potentials (`source code <https://github.com/electronicvisions/spikey_demo/blob/master/networks/epsp.py>`_).

.. todo:: regarding noise refer to Eric's publication
.. todo:: add tasks, e.g., compare synaptic time constants between exc and inh synapses

Lesson 2: Feedforward networks
------------------------------

.. todo:: add synfire chain here

Lesson 3: Recurrent networks
----------------------------

.. todo:: add decorrelation network here

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
.. [Petkov2012] Petkov, V. (2012). `Toward Belief Propagation on Neuromorphic Hardware <http://www.kip.uni-heidelberg.de/Veroeffentlichungen/download.php/5150/temp/2635-1.pdf>`_. Diploma thesis, Heidelberg University. HD-KIP 12-23.
.. [Gruebl2007] Grübl, A. (2007). `VLSI Implementation of a Spiking Neural Network <http://www.kip.uni-heidelberg.de/Veroeffentlichungen/download.php/4630/ps/agruebl_diss_kip.pdf>`_. PhD thesis, Heidelberg University. HD-KIP 07-10.
