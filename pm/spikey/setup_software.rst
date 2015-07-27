Setup Software
==============

When using the Spikey systems located at the UHEI cluster see :ref:`label-clusterlogin`.
On the cluster, the pre-built software package can be used, cf. :ref:`label-softwaremodule`.

The software build process is described in :ref:`label-spikeysoftware`.


.. _label-clusterlogin:

Login to UHEI Cluster
-----------------------


* from the KIP-institute network:

.. code-block:: bash

  ssh KIPUSER@{ice,ignatz}

* otherwise:

.. code-block:: bash

  ssh s1ext_someuser@gitviz.kip.uni-heidelberg.de:6022 # or 7022


.. _label-softwaremodule:

UHEI Cluster Software Module
-----------------------

.. todo:: Describe module environment thing here.

.. code-block:: bash

  module av
  module load pynn/whatever



.. _label-expexec:

Experiment execution
====================


.. _label-beforeexp:

Once before executing experiments
---------------------------------

.. todo:: will be replaced by a complete pynn.hardware.spikey module (with pre-built binaries)

Set environment variables:

.. code-block:: bash

  cd symap2ic
  . bootstrap.sh.UHEI

and load PyNN:

* On UHEI computer

.. code-block:: bash

  module load pynn/0.6.0-hw

* On private computer

  See :ref:`label-pynn`: ``export PYTHONPATH=...``


Run experiment
--------------

Download the `Spikey example experiment <https://github.com/electronicvisions/spikey_demo/blob/master/networks/example.py>`_.
For more network descriptions see `Spikey demos <https://github.com/electronicvisions/spikey_demo/blob/master/networks>`_.

* On UHEI cluster

.. code-block:: bash

  srun -p spikey --gres stationXXX python example.py

and replace XXX with the chip you want to use (e.g. 500).
For convenience you may consider adding an alias to your ~/.bashrc:

.. code-block:: bash

  echo "alias spikeyrun=\"srun -p spikey --gres stationXXX\"" >> ~/.bashrc

To view the queue of experiments:

.. code-block:: bash

  squeue

The list of available Spikeys on the UHEI cluster can be queried:

.. code-block:: bash

  srun --gres=help | grep ^station


* On private computer

.. code-block:: bash

  echo "stationXXX" > ~/my_stage1_station
  python example.py
