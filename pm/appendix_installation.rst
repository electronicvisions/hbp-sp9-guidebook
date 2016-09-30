========================================================
Appendix: Installation of the BrainScaleS software stack
========================================================

In the following the build and work flow on University of Heidelberg cluster frontend nodes is described.
This is only needed if you want to use the system locally within Heidelberg.
If the BrainScaleS System is accessed through the HBP Collaboratory or the Python client,
this software environment is pre-installed.

The following section can be skipped when loading the ``nmpm_software`` module by

.. code-block:: bash

    module load nmpm_software/current

All available versions can be listed by ``module avail nmpm_software``.

To compile your own installation create and change to a directory for
your projects, preferably on ``wang``, e.g.:
``/wang/users/<somebody>/cluster_home/projects``.


ssh-agent
'''''''''

To reduce the amount of typing, please consider using ``ssh-agent`` to cache your key password:

.. code-block:: bash

    eval `ssh-agent`
    ssh-add ~/path/to/your/private_id_rsa


Build Tool
''''''''''

We use a custom version (``git@gitviz.kip.uni-heidelberg.de:waf.git``) of the ``waf`` configuration and build tool.
A nightly version is provided by loading:

.. code-block:: bash

    module load waf


PyHMF, marocco and Dependencies
'''''''''''''''''''''''''''''''

The first step is to create a new workspace for the software checkouts and the subsequent build

.. code-block:: bash

    mkdir ~/my_nmpm_software && cd ~/my_nmpm_software

Now ``waf`` can be used to setup the project.
It will clone all the dependencies.

.. code-block:: bash

    waf setup --project pyhmf --project=marocco --without-ester

The next step is configuration.
As the default software environment on the UHEI cluster does not provide all the software dependencies, you have to load some modules which will provide those dependencies:

.. code-block:: bash

    module load localdir
    module load pynn/0.7.5
    module load mongo
    module load yaml-cpp/0.5.3

As those commands are needed every time you want to use the software it is convenient to put all the needed parts into a script:

.. code-block:: bash

    echo "INSTALLED_LIB_PATH=$(readlink -e lib)" > init.sh
    cat >>init.sh<<EOF
    cd ${INSTALLED_LIB_PATH}
    module load localdir
    module load pynn/0.7.5
    module load mongo
    module load yaml-cpp/0.5.3
    cd -
    EOF

After completing the installation steps below, this script can be sourced (``source init.sh``) to access the BrainScaleS Wafer-Scale Software Stack.

Now the configuration step:

.. code-block:: bash

    waf configure

The install step will build and install all targets into subdirectories of your current working directory.
Currently, you need to explicitly specify some extra targets in a second call.

.. code-block:: bash

    waf install --test-execnone
    # some extra targets are needed
    waf install --target=pymarocco,pyhalbe,pysthal,redman_xml --test-execnone

If you want to include the calibration toolkit (``cake``) (optional):

.. code-block:: bash

    waf setup --project pyhmf --project marocco --project cake --without-ester
    # module load ...
    waf configure
    waf install --test-execnone
    # some extra targets are needed
    waf install --target=pymarocco,pyhalbe,pysthal,redman_xml,pycake --test-execnone

To include support for executable system simulation (ESS) add ``--with-ess`` to the setup call.

Please remember, to that you have to setup the software environment if you start new shells (e.g. by using the  ``init.sh`` script):

.. code-block:: bash

    source ~/my_nmpm_software/init.sh

Check if the installation and the setup of variables is fine:

.. code-block:: bash

    python -c "import pyhmf" && echo ok

should print ``ok``, if instead:

.. code-block:: python

    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named pyhmf

occurs, either the installation failed or the environment variables responsible for finding the module are wrong.
In that case, double check if you followed the instructions 1:1.

Running PyNN scripts
''''''''''''''''''''

To run locally on the *hardware* one needs to use the SLURM job queue system:

.. code-block:: bash

       srun -p nmpm -L `license_by_hicann 33 367` --pty python nmpm1_single_neuron.py

nmpm1_single_neuron.py:

.. literalinclude:: examples/nmpm1_single_neuron.py

Inspect the Configuration
'''''''''''''''''''''''''

.. code-block:: bash

    sthal/tools/dump_cfg.py
