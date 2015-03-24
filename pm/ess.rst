===============================
Installation and use of the ESS
===============================

----------------------------------
Installation of the ESS (PyNN 0.8)
----------------------------------

By following this guideline, you will successfully install the current (as of March 2015) `stable` software stack of Heidelberg, containing the ESS, emulator of the NM-PM1 hardware system.
You will have installed it together with the compatible PyNN version (0.8).

Currently, a new software stack is under development which will replace the old one.


Prerequisites (tested on a native Ubuntu saucy 13.10 on a 64-bit machine)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    pip install scipy matplotlib PIL NeuroTools mpi4py xmlrunner

Then, you install nest:

.. code-block:: bash

    wget http://www.nest-initiative.org/download/gplreleases/nest-2.2.2.tar.gz
    tar xvzf nest-2.2.2.tar.gz
    cd nest-2.2.2
    ./configure --with-mpi --prefix=/opt/nest --with-pynest-prefix=/usr
    make
    make install
    python -c 'import nest'

You install pyNN (version 0.8 from the github NeuralEnsemble repository):

.. code-block:: bash

    cd
    git clone https://github.com/NeuralEnsemble/PyNN.git PyNN-8
    cd PyNN-8
    python setup.py install
    python -c 'import pyNN.nest as sim'


Installation of the ESS
^^^^^^^^^^^^^^^^^^^^^^^

You should first obtain an account from heidelberg_. Then, on your computer, you generate a rsa key:

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
    . bootstrap.sh.UHEI .
    ./waf set_config systemsim-pynn8
    ./waf update

If you have had problems in the execution of the 4 lines above, you have some read access right problems from the repositories.
Please consult Eric Müller or the person in charge from Heidelberg.
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

You test that the hardware backend is accessible:

.. code-block:: bash

    python -c 'import pyNN.hardware.brainscales as sim'

To test your installation, you can run the PyNN 0.8 unit- and system tests:

.. code-block:: bash

    cd ~/PyNN-8/test
    cd unittests/backends
    nosetests test_mock.py
    nosetests test_hardware_brainscales.py

.. _heidelberg: https://gitviz.kip.uni-heidelberg.de


----------------------------------
Installation of the ESS (PyNN 0.7)
----------------------------------


By following this guideline, you will successfully install the `stable` PyNN 0.7-based software stack of Heidelberg, containing the ESS, emulator of the BrainScaleS and of the Facets hardware.
You will have installed it together with the compatible PyNN version (0.7).


Prerequisites (tested on a native Ubuntu saucy 13.10 on a 64-bit machine)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to configure and compile the symap2ic project, you need to install the following libraries:

.. code-block:: bash

    apt-get -y install git python-pip python-dev build-essential libgtest-dev \
        libboost-all-dev libpng12-dev libssl-dev libmongo-client-dev mongodb \
        liblog4cxx10-dev autotools-dev automake
    pip install numpy

The ESS expects the 64-bit libraries to lie either in /lib64 or /usr/lib64.
However, in Ubuntu 13.10, the 64-bit libraries lie in /usr/lib/x86_64-linux-gnu.
So, you need to make the following symbolic links:

.. code-block:: bash

    ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
    ln -s /usr/lib/libmongoclient.a /usr/lib/x86_64-linux-gnu/libmongoclient.a

To be able to run the tests and to use the ESS, you also need to install:

.. code-block:: bash

    apt-get -y install libgsl0-dev libncurses5-dev libreadline-dev gfortran \
        libfreetype6-dev libblas-dev liblapack-dev r-base python-rpy
    pip install scipy matplotlib PIL NeuroTools mpi4py xmlrunner

Then, you install nest:

.. code-block:: bash

    wget http://www.nest-initiative.org/download/gplreleases/nest-2.2.2.tar.gz
    tar xvzf nest-2.2.2.tar.gz
    cd nest-2.2.2
    ./configure --with-mpi --prefix=/opt/nest --with-pynest-prefix=/usr
    make
    make install
    python -c 'import nest'

You install pyNN (version 0.7):

.. code-block:: bash

    pip install pyNN
    python -c 'import pyNN.nest as sim'


Installation of the ESS
^^^^^^^^^^^^^^^^^^^^^^^

You should first obtain an account from heidelberg_. Then, on your computer, you generate a rsa key:

.. code-block:: bash

    ssh-keygen -t rsa

Suppose that you have saved the key in the file ~/.ssh/id_rsa.
In the heidelberg_ website, you go to 'My account' (upper-right).
You click on 'Public Key' in the upper-right corner.
You click on 'New value' and paste the content of your computer's id_rsa.pub. Wait until the activation is done.

Then, you can download and install the ESS on your computer:

.. code-block:: bash

    cd
    git clone git@brainscales-r.kip.uni-heidelberg.de:symap2ic.git
    cd symap2ic
    . bootstrap.sh.UHEI .
    ./waf set_config systemsim

If you have had problems in the execution of the 4 lines above, you have some read access right problems from the repositories.
Please consult Eric Müller or the person in charge from Heidelberg.
Please now go on by configuring and installing the system:

.. code-block:: bash

    ./waf configure --stage=brainscales --use-systemsim --without-hardware \
        --prefix=$SYMAP2IC_PATH
    ./waf install

You now set the environment variables:

.. code-block:: bash

    echo 'export SYMAP2IC_PATH=$HOME/symap2ic' >> ~/.bashrc
    echo 'export PYTHONPATH=$PYTHONPATH:$SYMAP2IC_PATH/lib' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SYMAP2IC_PATH/lib' >> ~/.bashrc
    bash

You copy the pyNN hardware directory into pyNN:

.. code-block:: bash

    cd $SYMAP2IC_PATH
    cp -r components/pynnhw/misc/pyNN_hardware_patch/hardware \
        /usr/local/lib/python2.7/dist-packages/pyNN/
    python -c 'import pyNN.hardware.brainscales as sim'

To test your installation, you can run some unit tests:

.. code-block:: bash

    python $SYMAP2IC_PATH/components/mappingtool/test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/regression/run_ess_tests.py
    python $SYMAP2IC_PATH/components/systemsim/test/system/run_ess_tests.py

.. _heidelberg: https://gitviz.kip.uni-heidelberg.de
