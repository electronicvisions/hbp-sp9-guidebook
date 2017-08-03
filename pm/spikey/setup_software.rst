Experiment execution
====================

Use the following instructions to login, load the pre-built software package and run experiments on the UHEI cluster.
For using the Spikey system outside the UHEI cluster and for developers, please manually install the required software (see :ref:`label-spikeysoftware`).


.. _label-clusterlogin:

Login to UHEI cluster
---------------------

* From the network of the Kirchhoff-Institute for Physics:

.. code-block:: bash

  ssh KIPUSER@hel

* Otherwise:

.. code-block:: bash

  ssh s1ext_someuser@gitviz.kip.uni-heidelberg.de -p 11022


.. _label-softwaremodule:

Load software modules
---------------------

To load the pre-built software package and configure the environment variables use:

.. code-block:: bash

  . /wang/environment/software/jessie/spack/current/share/spack/setup-env.sh
  spack load --dependencies visionary-defaults 
  module load spikey

These three commands must be loaded for every environment, and in particular, after logging in.


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

To select a chip using the `web interface of the Human Brain Project <https://www.hbpneuromorphic.eu/home.html>`_ enter the following parameters into the "Hardware Config" box:

.. code-block:: none

  {"STATION":"stationXXX"}

Replace XXX with the number of the chip you want to use (e.g. 500).


Visualization of the chip configuration
---------------------------------------

What is the *scvisual* tool?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The tool *scvisual* (for "spikey config visualization") displays a visualization of the almost complete hardware configuration of an experiment. It loads data from the file "spikeyconfig.out" which is generated during experiment execution in your working directory. The program *scvisual* enables you to

* investigate the full network connectivity of a Spikey experiment, 
* zoom into details of both 256x192-sized synapse arrays,
* hover over neurons and synapse drivers to inspect their configuration,
* retrieve detailed information on most analog hardware parameters,
* compare the displayed configuration with a photo of the chip, and
* save high-resolution png figures of you network configuration to disk.

The tool is written in python and makes extensive use of the interactive functionality of matplotlib.


Who can benefit from *scvisual*?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The tool is designed for both novice and experienced users.
If you are new to using the Spikey system, *scvisual* gives you an impression of where the physical model neurons and synapses are actually located on the chip.
To our experience, the tool can further be very helpful to expert users for developing and debugging PyNN-based experiment descriptions.


Installation and usage
^^^^^^^^^^^^^^^^^^^^^^

**For local users**
  | Users located at the institute or operating "their own" Spikey chip at a local computer [1]_ simply type:
  |
  |   *$ scvisual*
  |
  | in the working directory after the experiment is completed. 

**For remote users**
  | The ssh connection will likely not support remote execution of the interactive graphical interface. The good news is: you can still run the program on your local machine -- even without a full software installation. From
  |
  |   https://github.com/electronicvisions/spikeyhal/tree/flyspi/tools
  |
  | download the following files: *scvisual.py, scparse.py, spikey_gold_label_medium.png*.
    Then rename *scvisual.py* to *scvisual*, set *scvisual* to be executable, and make all files available in your *$PATH* and *$PYTHONPATH*. Now
  |
  |   $ scvisual
  |
  | should work in any local directory that contains a "spikeyconfig.out" file.

**Additonal options**
  | The 'pure' command *scvisual* will load the experiment configuration from 
    "spikeyconfig.out" with reasonable plotting options. For a description of additional options type:
  |
  |   *$ scvisual -h*


Footnotes
^^^^^^^^^

.. [1] More precisely, access to a local installation of the operation software is required. For installation instructions see :ref:`label-spikeysoftware`.