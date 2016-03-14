Experiment execution
====================

Use the following instructions to login, load the pre-built software package and run experiments on the UHEI cluster.
For using the Spikey system outside the UHEI cluster and for developers, please manually install the required software (see :ref:`label-spikeysoftware`).


.. _label-clusterlogin:

Login to UHEI cluster
---------------------

* From the network of the Kirchhoff-Institute for Physics:

.. code-block:: bash

  ssh KIPUSER@{ice,ignatz}

* Otherwise:

.. code-block:: bash

  ssh s1ext_someuser@gitviz.kip.uni-heidelberg.de -p 7022 # or 6022


.. _label-softwaremodule:

Load software modules
---------------------

To load the pre-built software package and configure the environment variables use:

.. code-block:: bash

  module load spikey

This module has to be loaded for every environment, and in particular, after logging in.


.. _label-expexec:

Run experiment
--------------

Download the `Spikey example experiment <https://github.com/electronicvisions/spikey_demo/blob/master/networks/example.py>`_.
For more example networks see :ref:`label-spikeyschool` and `Spikey demos <https://github.com/electronicvisions/spikey_demo/blob/master/networks>`_.
On the UHEI cluster `SLURM <http://slurm.schedmd.com/>`_ is used to manage the workload on our systems.
To queue the execution of a Python script use:

.. code-block:: bash

  srun -p spikey --gres stationXXX python example.py

Replace XXX with the number of the chip you want to use (e.g. 500).


Tips and tricks
---------------

* To view the queue of experiments use:

.. code-block:: bash

  squeue

* To query a list of available Spikey systems on the UHEI cluster see the `chip status page <https://gitviz.kip.uni-heidelberg.de:8443/view/spikey/job/hw_spikey_chipstatus_all/>`_.

* The setup of SSH keys for pubkey-based access to github.com is described in :ref:`label-clustersshkeygithub`.


Using the web interface of the Human Brain Project
--------------------------------------------------

To select a chip using the `web interface of the Human Brain Project <https://www.hbpneuromorphic.eu>`_ enter the following parameters into the "Hardware Config" box:

.. code-block:: none

  {"STATION":"stationXXX"}

Replace XXX with the number of the chip you want to use (e.g. 500).
