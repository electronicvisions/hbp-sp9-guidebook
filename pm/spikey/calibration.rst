Built-in calibrations
=====================

The calibration of the Spikey neuromorphic system consists of five components:

* Calibration of fast analog-to-digital converter (for recording analog signals)

* Calibration of parameter cells (vout values)

* Calibration of output pins (for reading out analog signals)

* Calibration of membrane time constant

* Calibration of refractory period (currently not used)

* Calibration of synapse drivers (axon-wise adjustment of synaptic strength, see also [Pfeil2013]_)

To calibrate the chip get source code

.. code-block:: bash

  git clone https://github.com/electronicvisions/spikey-calib.git

and run the calibration

.. code-block:: bash

  python calibAll.py stationXXX

where XXX has to be replaced by the chip number to be calibrated.

To visualize calibration results run

.. code-block:: bash

  python analyzeAll.py stationXXX
