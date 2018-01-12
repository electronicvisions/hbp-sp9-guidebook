=======================================
The HBP Neuromorphic Computing Platform
=======================================

Living document version:

.. include:: gitversion.rst_tochide

.. [Initial paragraph needs to be kept short]

The Neuromorphic Computing Platform allows neuroscientists and engineers to perform experiments with configurable neuromorphic computing systems.
The platform provides two complementary, large-scale neuromorphic systems built in custom hardware at locations in Heidelberg, Germany (the "BrainScaleS" system, also known as the "physical model" or PM system) and Manchester, United Kingdom (the "SpiNNaker" system, also known as the "many core" or MC system). Both systems enable energy-efficient, large-scale neuronal network simulations with simplified spiking neuron models. The BrainScaleS system is based on physical (analogue) emulations of neuron models and offers highly accelerated operation (10\ :superscript:`4` x real time). The SpiNNaker system is based on a digital many-core architecture and provides real-time operation.

These large-scale neuromorphic systems are currently in their commissioning phase, which is accompanied by short technology and software switchover times. In order to ensure that obtained results are up to date and valid, we kindly request all users to review all material intended for dissemination (websites, papers etc.) with the involved groups.

.. toctree::
   :maxdepth: 2

   quick_start
   building_models
   using_the_platform
   pm/pm
   pm/spikey
   mc/mc_index
   benchmarks
   getting_help
   pm/appendix_installation.rst
   appendix
   reference/python_client
