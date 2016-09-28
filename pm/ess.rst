===================================
Simulating the BrainScaleS hardware
===================================

The Executable System Specification (ESS) is a software model of the BrainScaleS hardware system.
The ESS is implemented in C++/SystemC and contains functional models of all relevant units of the wafer-scale hardware.
It is fully executable and resembles how neural experiments are run on the real wafer-scale system.

The ESS allows offline experimentation with the BrainScaleS system, and can be used for testing
small models locally before submitting them to the hardware system, and for introspecting the
system behaviour. The ESS supports PyNN versions 0.7 and 0.8.

Note, however, that the ESS runs *much* more slowly than the real hardware.


Installation
============

Using Docker
````````````

The simplest way to use the ESS is to use the (`uhei/ess-system
<https://registry.hub.docker.com/u/uhei/ess-system>`_) Docker image.
This has a recent version of the ESS already installed, and is updated on a regular basis.

Prerequisites
-------------

You need to have Docker installed.
On Ubuntu Trusty 14.04 LTS the Docker package is called ``docker.io``.
Note that there is a package named ``docker`` in the Ubuntu repositories as well.
It is something completely different.

After installing you may add yourself to the ``docker`` group.
Otherwise you have to prepend sudo to most Docker commands.

You might also want to have a look at ``/etc/default/docker.io`` after installation, especially if you're sitting behind a proxy.
These proxy settings are not for the containers, but for communication with the Docker Repository (i.e. docker pull).

.. code-block:: bash

    sudo apt-get install docker.io
    # sudo adduser $USER docker
    # sudo editor /etc/default/docker.io
    # re-login


Download/upgrade of the uhei/ess-system image
---------------------------------------------

The following step takes some time upon first execution, depending on your internet connection.
Later updates should generally perform faster as only changes are pulled.

.. code-block:: bash

    sudo docker pull uhei/ess-system:14.04


Starting the ESS container
--------------------------

The execution of the downloaded image creates a new Docker container.
Note that Docker containers are not persistent,
but one can link a host directory for persistent user data into the container.
The following ``docker run`` command does just that.
The host directory specified by the ``VOLUME`` environment variable will be available as ``/bss/$USER`` within the container.
If you're interested in the option flags of the ``docker run`` command, run ``docker help run``.

.. code-block:: bash

    # docker help run
    mkdir ess-data                # where to put user/persistent data
    VOLUME="${PWD}/ess-data"
    sudo docker run --name ess-container --hostname ess-container \
            -v "$VOLUME:/bss/$USER" -ti "uhei/ess-system:14.04" /bin/bash


Testing your ESS container installation
---------------------------------------

You should be in the container now, as ``root`` in the directory ``/bss`` (as in BrainScaleS).
An ``ls`` should show your folder for persistent data
(under your user name or whatever you put instead of ``$USER`` in the ``docker run`` command above),
as well as the directories ``mappingtool_test``, ``neurotools`` and ``tutorial``.

To test your installation, you can run some unit tests.
This is almost the same as with the installation below,
just the mapping tool test is installed at another location:

.. code-block:: bash

    # root@ess-container:/bss#
    python mappingtool_test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/system/run_ess_tests.py


Installing from source
``````````````````````

.. note:: these instructions have been tested on a native Ubuntu saucy 13.10 on a 64-bit machine

Prerequisites
-------------

To be able to configure and compile the symap2ic project, you need to install the following libraries:

.. code-block:: bash

    apt-get -y install git python-pip python-dev build-essential libgtest-dev \
        libboost-all-dev libpng12-dev libssl-dev libmongo-client-dev mongodb \
        liblog4cxx10-dev autotools-dev automake

The ESS expects the 64-bit libraries to lie either in /lib64 or /usr/lib64.
However, in Ubuntu 13.10, the 64-bit libraries lie in /usr/lib/x86_64-linux-gnu.
So, you need to make the following symbolic links:

.. code-block:: bash

    ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
    ln -s /usr/lib/libmongoclient.a /usr/lib/x86_64-linux-gnu/libmongoclient.a

To be able to run the tests and to use the ESS, you also need to install:

.. code-block:: bash

    apt-get -y install libgsl0-dev libncurses5-dev libreadline-dev gfortran \
        libfreetype6-dev libblas-dev liblapack-dev r-base python-rpy \
    pip install numpy scipy matplotlib PIL NeuroTools mpi4py xmlrunner

You should then install PyNN:

.. code-block:: bash

    pip install PyNN  # PyNN 0.8

or

.. code-block:: bash

    pip install PyNN==0.7.5  # PyNN 0.7


Installation of the ESS
-----------------------

You should first obtain an account from the heidelberg_ group. Then, on your computer, you generate a rsa key:

.. code-block:: bash

    ssh-keygen -t rsa

Suppose that you have saved the key in the file ~/.ssh/id_rsa. In the heidelberg_ website, you go to 'My account' (upper-right).
You click on 'Public Key' in the upper-right corner.
You click on 'New value' and paste the content of your computer's id_rsa.pub.
Wait until the activation is done.

Then, you can download and install the ESS on your computer:

.. code-block:: bash

    cd
    git clone git@brainscales-r.kip.uni-heidelberg.de:symap2ic.git
    cd symap2ic
    source bootstrap.sh.UHEI .

For PyNN 0.8:

.. code-block:: bash

    ./waf set_config systemsim-pynn8
    ./waf update

For PyNN 0.7:

For PyNN 0.8:

.. code-block:: bash

    ./waf set_config systemsim

If you have had problems in the execution of the 4 lines above, you have some read access right problems from the repositories.
Please e-mail neuromorphic@humanbrainproject.eu.
Please now go on by configuring and installing the system:

.. code-block:: bash

    ./waf configure --stage=brainscales --use-systemsim --without-hardware \
        --prefix=$HOME/symap2ic
    ./waf install

You now set the environment variables:

.. code-block:: bash

    echo 'export SYMAP2IC_PATH=$HOME/symap2ic' >> ~/.bashrc
    echo 'export PYTHONPATH=$PYTHONPATH:$SYMAP2IC_PATH/lib' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SYMAP2IC_PATH/lib' >> ~/.bashrc
    bash

For PyNN 0.7, you need to copy the PyNN hardware directory into the PyNN package:

.. code-block:: bash

    cd $SYMAP2IC_PATH
    cp -r components/pynnhw/misc/pyNN_hardware_patch/hardware \
        /usr/local/lib/python2.7/dist-packages/pyNN/

You can now test that the hardware backend is accessible:

.. code-block:: bash

    python -c 'import pyNN.hardware.brainscales as sim'

To test your installation with PyNN 0.7, you can run some unit tests:

.. code-block:: bash

    python $SYMAP2IC_PATH/components/mappingtool/test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/system/run_ess_tests.py

To test your installation with PyNN 0.8, you can run the PyNN unit and system tests:

.. code-block:: bash

    cd ~/PyNN-8/test
    cd unittests/backends
    nosetests test_mock.py
    nosetests test_hardware_brainscales.py


Using the ESS
=============

Scripts to run on the ESS should in general be identical to those that run on the BrainScaleS hardware. The only required
difference is that the :func:`setup()` call must include the argument ``useSystemSim=True``.

In addition, there is an optional argument ``ess_params``, which should be a dictionary containing the following
parameters:

``perfectSynapseTrafo``
   Use a perfect synapse transformation, instead of the only available ideal synapse transformation [boolean].

``weightDistortion``
   Specifies the distortion of synaptic weights in the virtual hardware system.

   This parameters define the fraction of the original value, that is used as
   the standard deviation for randomizing the weight according to a normal
   distribution around the original value.

``pulseStatisticsFile``
    Name of file to which the ESS pulse statistics are written.


Perfect Synapse Transformation
``````````````````````````````

Currently, there exists only one set of calibration data for the transformation of synaptic weights to the hardware.
i.e., there is only one configuration of the synapse drivers, for which a calibration has been done in ideal transistor-level hardware simulations, such that one is restricted to exactly 16 different synaptic weight settings in the hardware.

But, in principle, one can use different settings for the synapse drivers to allow a wider range of synaptic weights. This will be available in the near future.

In order to already mimic this behavior with the ESS, one can choose the "perfect synapse transformation", which generates different configurations of the synapse driver such that the associated synaptic weights match those specified in PyNN, at least within the 4-bit resolution of the digital weights.

.. code-block:: python

    sim.setup(useSystemSim=True, ess_params={'perfectSynapseTrafo':True})


Pulse Loss Statistics
`````````````````````

The ESS allows to count all spikes that were lost in any place of the virtual hardware system.
Spikes are mostly lost in the off-wafer communication network (also called ''Layer 2 network'') that connects the wafer to the host PC.
In the Layer 2 network pulse loss can happen on two routes:

1. Stimulation:
   not all spikes from the spike sources (:class:`SpikeSourcePoisson` or :class:`SpikeSourceArray`) are delivered to its targets, because the bandwidth in the off-wafer network is limited. When a spike is lost, it is lost for its targets.

2. Recording:
   For the same bandwidth constraints in the off-wafer network, some spikes of real neurons can be lost on the route from the wafer to the FGPGAs, Hence, in the received spike data some events are missing.
   However, the 'non-recorded' spikes did reach their target neurons on the wafer.

Spikes can also be lost on the wafer, but only in rare cases when many neuron located on the same HICANN fire synchronously.

3. On-wafer Spike Loss:
   This is the case of pulses lost in the on-wafer pulse-communication system (also called `Layer 1 network`). If this happens, spikes are completely deleted, and reach no other neuron.

4. Spike Drop before Simulation:
   The playback module of the FPGA, which plays back the stimuli pulses at given times, also has a limited bandwidth. This limitation is considered beforehand, such that spikes are dropped even before the simulation, in order to avoid a further delaying of many more spikes during an experiment.

The ESS counts the lost and sent pulses.
After the simulation, you will see something in the log for a loglevel>=2::

    INFO  Default *************************************
    INFO  Default LostEventLogger::summary
    INFO  Default Layer 2 events dropped before sim : 837/3939 (21.249 %)
    INFO  Default Layer 2 events lost :               243/3199 (7.59612 %)
    INFO  Default Layer 2 events lost downwards :     243/3102 (7.83366 %)
    INFO  Default Layer 2 events lost upwards   :     0/97 (0 %)
    INFO  Default Layer 1 events lost : 0/79 (0 %)
    INFO  Default *************************************


You can specify to get this data by specifying a file ``pulseStatisticsFile`` in the setup command:

.. code-block:: python

    sim.setup(useSystemSim=True, ess_params={'pulseStatisticsFile': 'pulse_stats.py'})


Then the pulse statistics file contains a Python dictionary ``pulse_statistics`` which can be use for further processing:

.. code-block:: python

    pulse_statistics = {
    'l2_down_before_sim': 3939,
    'l2_down_dropped_before_sim': 837,
    'l2_down_sent': 3102,
    'l2_down_lost': 243,
    'l2_up_sent': 97,
    'l2_up_lost': 0,
    'l1_neuron_sent': 79,
    'l1_neuron_lost': 0,
    }


.. _heidelberg: https://gitviz.kip.uni-heidelberg.de
