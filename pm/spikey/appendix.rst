Spikey Appendix
===============

.. _label-clustersshkeygithub:

Setting up SSH keys on UHEI cluster for github.com
--------------------------------------------------

To create a key pair please follow the guide provided by github.com.
The configuration file for the ssh connection is located in ``~/.ssh/config``.
For example:

.. code-block:: bash

  $ cat .ssh/config
  Host github.com
      IdentityFile /wang/users/USERNAME/.ssh/my_github.com.id_rsa

The ``Host github.com`` describes the ``ssh`` connection target, and the following line
configures the private key location which will be used for this target host.

To connect via ssh, use the ``tsocks`` tool which routes the TCP connection via a local SOCKS proxy, e.g.:

.. code-block:: bash

  $ tsocks git clone git@github.com:USERNAME/PROJECT.git



.. _label-spikeysoftware:

Setup software
--------------


Preparing the operating system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We consider the newest stable `Debian <http://www.debian.org>`_ operating system as reference system.

The following additional software packages are required for building the software of the Spikey system:

.. code-block:: bash

  sudo apt-get install libboost-all-dev libusb-1.0-0-dev liblog4cxx10-dev libqt4-dev libgtest-dev libgsl0-dev python-nose

And for experiment execution:

.. code-block:: bash

  sudo apt-get install python-numpy python-scipy python-matplotlib


Installing hardware drivers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The software for the Spikey neuromorphic system is managed by a git repository that can be downloaded as follows:

.. code-block:: bash

  git clone https://github.com/electronicvisions/spikey_demo.git

To install the software follow the instructions in the ``README.md`` file.
Note that a fork of the official `PyNN <http://neuralensemble.org/PyNN/>`_ project is used that builds on PyNN version 0.6.


Allow access to USB device
^^^^^^^^^^^^^^^^^^^^^^^^^^

To access the Spikey system via USB, add your user to the ``plugdev`` UNIX group, to which Spikey devices are assigned to.
Note that you will need root privileges for adding users to a UNIX group.

#. Add your user to ``plugdev`` group: ``sudo usermod -aG plugdev USERNAME`` (replace USERNAME)
#. Assign Spikey systems to ``plugdev`` group (creates a ``udev`` config file): ``sudo sh vmodule/nosudo``
#. Restart ``udev`` daemon: ``service udev restart`` and (re-)plug-in the Spikey USB device.

.. commenting out a todo:: enable usage of Spikey systems without root privileges


Run experiments
^^^^^^^^^^^^^^^

Set environment variables (has to be done only once for each environment):

.. code-block:: bash

  . bin/env.sh

Run PyNN description of a network:

.. code-block:: bash

  cd networks
  python example.py


Miscellaneous
^^^^^^^^^^^^^

If multiple chips are connected to a single host computer, use environment variables to select the chip:

.. code-block:: bash

  MY_STAGE1_STATION=stationXXX

Replace XXX with the chip you want to use (e.g. 500).



Setup hardware
--------------

`Link <https://gitviz.kip.uni-heidelberg.de/projects/symap2ic/wiki/Hardware_setup>`_ to internal web page.
