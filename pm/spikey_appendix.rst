------
Spikey
------

.. _label-spikeysoftware:

Spikey software
===============


Preparing the operating system
------------------------------

We consider the newest stable `Ubuntu <http://www.ubuntu.com/desktop>`_ operating system as reference system.

The following additional software packages are required for building the software of the Spikey system:

.. code-block:: bash

  sudo apt-get install libboost-all-dev libusb-1.0-0-dev liblog4cxx10-dev libqt4-dev libgtest-dev libgsl0-dev python-nose

And for experiment execution:

.. code-block:: bash

  sudo apt-get install python-numpy python-scipy python-matplotlib


Installing hardware drivers
---------------------------

The driver software of the Spikey system is managed by a software repository called "symap2ic".
Note that you need an account for the `UHEI project management system <https://gitviz.kip.uni-heidelberg.de/>`_ to access this repository.
To install the software follow these instructions step by step:

#. Add ssh key for authentication (for help see `here <https://gitviz.kip.uni-heidelberg.de/projects/symap2ic/wiki/Symap2icGitvizHowto>`_)
#. Download the root repository: ``git clone git@gitviz.kip.uni-heidelberg.de:symap2ic.git``
#. ``cd symap2ic``
#. Set environment variables: ``. bootstrap.sh.UHEI``
#. Choose your software configuration: ``./waf set_config stage1-flyspi-single``
#. Install the software: ``./waf configure build install``
#. If using multiple chips connected to a single host computer: ``echo "stationXXX" > ~/my_stage1_station`` and replace XXX with the chip you want to use (e.g. 500).


.. _label-pynn:

Installing PyNN
---------------

The Spikey system is not yet included as a back end in the official `PyNN <http://neuralensemble.org/PyNN/>`_ project.
So please download and install a Spikey-specific PyNN version which builds on PyNN version 0.6.0.

#. Download the source code: ``git clone git@gitviz.kip.uni-heidelberg.de:deb-pynn``
#. ``cd deb-pynn``
#. Select branch: ``git checkout 0.6.0``
#. Install PyNN to the installation path DIR: ``python setup.py install --prefix=DIR``
#. Add the following line to your bashrc: ``export PYTHONPATH=$PYTHONPATH:DIR/lib/pythonX.Y/site-package`` (replace DIR, X, Y, respectively)


Allow access to USB device
--------------------------

To access the Spikey system via USB, add your user to the ``plugdev`` group, to which Spikey devices are assigned to.
Note that you will need root privileges for adding users to a group.

#. Add your user to ``plugdev`` group: ``sudo usermod -aG plugdev USERNAME`` (replace USERNAME)
#. Assign Spikey systems to ``plugdev`` group: ``cd symap2ic; sudo sh components/vmodule/nosudo``

.. todo:: enable usage of Spikey systems without root privileges


Once before executing experiments
---------------------------------

Set environment variables:

.. code-block:: bash

  cd symap2ic
  . bootstrap.sh.UHEI

Ensure that your ``PYTHONPATH`` is set correctly (see :ref:`label-pynn`).


Run experiment
--------------

.. code-block:: bash

  python example.py
