.. _label-spikeysoftware:

Spikey Software
===============

Preparation of operating system
-------------------------------

We consider the newest stable `Ubuntu <http://www.ubuntu.com/desktop>`_ operating system as reference system.

Software packages required for build:

.. code-block:: bash

  sudo apt-get install libboost-all-dev libusb-1.0-0-dev liblog4cxx10-dev libqt4-dev libgtest-dev libgsl0-dev python-nose

Software packages required for experiment execution:

.. code-block:: bash

  sudo apt-get install python-numpy python-scipy python-matplotlib

Installing hardware drivers
---------------------------

The driver software for the Spikey system is managed by the repository called "symap2ic".
Note that you need an account for the `project management system <https://gitviz.kip.uni-heidelberg.de/>`_ in Heidelberg to access this repository.
To get access, download and install the driver software process the following instructions step by step:

#. Add ssh key for authentication (for help see `here <https://gitviz.kip.uni-heidelberg.de/projects/symap2ic/wiki/Symap2icGitvizHowto>`_)
#. Download the root repository: ``git clone git@gitviz.kip.uni-heidelberg.de:symap2ic.git``
#. ``cd symap2ic``
#. Set environment variables: ``. bootstrap.sh.UHEI``
#. Choose your software configuration: ``./waf set_config stage1-flyspi-single``
#. Install the software: ``./waf configure build install``
#. If using multiple chip connected to single host computer, create a file named "my_stage1_station" in your home directory and enter your default station (e.g., "station500")

.. _label-pynn:


Installing PyNN
---------------

The Spikey backend is not included in the official `PyNN <http://neuralensemble.org/PyNN/>`_ project.
So please download and install a Spikey-specific PyNN version which builds on PyNN version 0.6.0.

* On UHEI computer

.. code-block:: bash

  module load pynn/0.6.0-hw

* On private computer

#. Download the source code: ``git clone git@gitviz.kip.uni-heidelberg.de:deb-pynn``
#. ``cd deb-pynn``
#. Select branch: ``git checkout 0.6.0``
#. Install PyNN to the installation path DIR: ``python setup.py install --prefix=DIR``
#. Add the following line to your bashrc: ``export PYTHONPATH=$PYTHONPATH:DIR/lib/pythonX.Y/site-package`` (replace DIR, X, Y, respectively)

Allow access to USB device
--------------------------

If using the Spikey system on a private computer, you will need root privileges to allow normal users to access this USB device.

#. Add your user to ``plugdev`` group: ``sudo usermod -aG plugdev USERNAME`` (replace USERNAME)
#. Assign Spikey systems to ``plugdev`` group: ``cd symap2ic; sudo sh components/vmodule/nosudo``


