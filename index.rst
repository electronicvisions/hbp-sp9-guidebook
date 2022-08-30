=======================================
The HBP Neuromorphic Computing Platform
=======================================

Document version:

.. include:: gitversion.rst_tochide

.. [Initial paragraph needs to be kept short]

The Neuromorphic Computing systems SpiNNaker and BrainScaleS allow neuroscientists and engineers to perform experiments with configurable neuromorphic computing systems.
The systems are part of the `EBRAINS research infrastructure`_. The EBRAINS infrastructure is created by the `Human Brain Project`_ (HBP). After the end of HBP (i.e. after September 2023) the research infrastructure operation will be continued by the EBRAINS AISBL legal entity.

The two complementary, large-scale neuromorphic systems built in custom hardware at locations in Heidelberg, Germany (the "BrainScaleS" system, also known as the "physical model" or PM system) and Manchester, United Kingdom (the "SpiNNaker" system, also known as the "many core" or MC system). Both systems enable energy-efficient, large-scale neuronal network simulations with simplified spiking neuron models. The BrainScaleS system is based on physical (analogue) emulations of neuron models and offers highly accelerated operation (10\ :superscript:`3` x real time in the BrainScaleS-2 version). The SpiNNaker system is based on a digital many-core architecture and provides real-time operation.

SpiNNaker and BrainScaleS soft- and hardware are under active development. In order to ensure that obtained results are up to date and valid, we kindly request all users to review all material intended for dissemination (websites, papers etc.) with the involved groups.

.. toctree::
   :maxdepth: 2

   quick_start
   building_models
   using_the_platform
   pm/pm
   pm/spikey
   pm/bss2
   mc/mc_index
   benchmarks
   getting_help
..   pm/appendix_installation.rst
..   appendix
   reference/python_client


.. _`EBRAINS research infrastructure`: https://ebrains.eu/service/neuromorphic-computing
.. _`Human Brain Project`: https://www.humanbrainproject.eu/
