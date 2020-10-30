Experiment execution
====================

Use the following instructions to login, load the pre-built software package and run experiments on the UHEI cluster.


.. _label-clusterlogin_bss2:

Login to UHEI cluster
---------------------

* From the network of the Kirchhoff-Institute for Physics:

.. code-block:: bash

  ssh KIPUSER@hel

* Otherwise:

.. code-block:: bash

  ssh s1ext_someuser@gitviz.kip.uni-heidelberg.de -p 11022


.. _label-software_bss2:

Load and build software
-----------------------

To load and build software for the BSS-2 system these modules are needed. Get them by using:

.. code-block:: bash

  module load waf
  module load ppu-toolchain
  module load localdir

These three commands must be loaded for every environment, and in particular, after logging in.

To checkout all important software repositories use:

.. code-block:: bash

  # leave out the --repo-db-url=... parameter to use the "UHEI-internal" repositories
  waf setup --project template-experiment-dls --repo-db-url=https://github.com/electronicvisions/projects

To build the software use:

.. code-block:: bash

  srun -p compile -c 8 --pty singularity exec --app visionary-dls /containers/stable/latest waf configure install

