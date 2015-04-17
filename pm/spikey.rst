=================
Use of the Spikey
=================

.. todo:: this will be extended by Thomas Pfeil, soon 


Setup software
==============

Preparation
-----------

.. todo:: add how to install pynn


Run experiments
===============

Once before executing experiments
---------------------------------

Set environment variables:

.. code-block:: bash

  cd symap2ic
  . bootstrap.sh.UHEI

and load PyNN:

* On Heidelberg computer

.. code-block:: bash

  module load pynn/0.6.0-hw

* On private computer

.. code-block:: bash

  export PYTHONPATH=... (see above)

Run experiment
--------------

Download the `Spikey example experiment`.
For more network descriptions see `Spikey demos`.

* On Heidelberg computer

.. code-block:: bash

  srun -p spikey --gres spikeyXXX python example.py

and replace XXX with the chip you want to use (e.g. 500).
For convenience you may consider adding an alias to your ~/.bashrc:

.. code-block:: bash

  echo "alias spikeyrun=\"srun -p spikey --gres SpikeyXXX\"" >> ~/.bashrc

To view the queue of experiments:

.. code-block:: bash

  squeue

* On private computer

.. code-block:: bash

  echo "stationXXX" > ~/my_stage1_station
  python example.py

.. _`Spikey example experiment`: https://github.com/electronicvisions/spikey_demo/blob/master/networks/example.py
.. _`Spikey demos`: https://github.com/electronicvisions/spikey_demo/blob/master/networks/example.py
