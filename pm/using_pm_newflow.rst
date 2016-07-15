=============================
Wafer Scale Mapping (Marocco)
=============================

Wafer Scale Mapping is performed by ``marocco`` and described in the `PhD thesis of S. Jeltsch`_.

.. _PhD thesis of S. Jeltsch: http://www.kip.uni-heidelberg.de/Veroeffentlichungen/details.php?id=3052

Code documentation is provided by ``doxygen`` and available as `documentation-marocco`_.

.. _documentation-marocco: https://brainscales-r.kip.uni-heidelberg.de:8443/view/doc/job/doc-dsl_marocco/marocco_Documentation

In the following the build and work flow on UHEI BrainScaleS cluster
frontend nodes is described. If the BrainScaleS is accessed through the
Collaboratory or the Python client, the installation can be skipped.

Installation
------------

Create and change to a directory for your projects, preferably on ``wang``, e.g.: ``/wang/users/<somebody>/cluster_home/projects``.


ssh-agent
'''''''''

To reduce the amount of typing, please consider using ``ssh-agent`` to cache your key password:

.. code-block:: bash

    eval `ssh-agent`
    ssh-add ~/path/to/your/private_id_rsa


waf
'''

This step is optional as the default environment already provides a ``waf`` executable.
However, if you need a customized waf version:

.. code-block:: bash

    git clone git@gitviz.kip.uni-heidelberg.de:waf.git -b symwaf2ic visions-waf
    make -f visions-waf/Makefile
    ln -f visions-waf/waf .
    alias waf=$PWD/waf



pyhmf, marocco and dependencies
'''''''''''''''''''''''''''''''

Then create and change to a directory for marocco, e.g., ``/wang/users/somebody/cluster_home/projects/marocco``:

.. code-block:: bash

    waf setup --project pyhmf --project=marocco --without-ester
    waf configure
    waf install --test-execnone
    # some extra targets are needed
    waf install --target=pymarocco,pyhalbe,pysthal,redman_xml --test-execnone

including cake (optional):

.. code-block:: bash

    waf setup --project pyhmf --project marocco --project cake --without-ester
    waf configure
    waf install --test-execnone
    # some extra targets are needed
    waf install --target=pymarocco,pyhalbe,pysthal,redman_xml,pycake --test-execnone

including support for ESS add ``--with-ess`` to setup call.


paths
'''''

To include the local paths in your environment, please use:

.. code-block:: bash

   module load localdir
   module load pynn/0.7.5
   module load mongo
   module load yaml-cpp/0.5.2

Another method would be to create an init file and put all the needed parts into a script:

.. code-block:: bash

    echo "INSTALLED_LIB_PATH=$(readlink -e lib)" > init.sh
    cat >>init.sh<<EOF
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:\${INSTALLED_LIB_PATH}
    export PYTHONPATH=$PYTHONPATH:\${INSTALLED_LIB_PATH}
    module load pynn/0.7.5
    module load mongo
    module load yaml-cpp/0.5.2
    EOF

In every (!) fresh shell you now have to source the ``init.sh``:

.. code-block:: bash

    source path/to/init.sh

Check if the installation and the setup of variables is fine:

.. code-block:: bash

    python -c "import pyhmf" && echo ok

should print ``ok``, if instead:

.. code-block:: python

    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named pyhmf

occurs, either the installation failed or the environment variables responsible for finding the module are wrong. In that case, double check if you followed the instructions 1:1.


Usage
-----

``pyhmf`` is the C++ implementation of ``pynn`` for the NMPM1. To
allow you to change the simulation/emulation backend easily, it is
adviced to give the ``pyhmf`` module an other name like ``pynn``:

.. code-block:: python

		import pyhmf as pynn

We also need the helper module ``pymarocco`` that takes care of
hardware and marocco specific settings:

.. code-block:: python

		import pyhmf as pynn
		from pymarocco import PyMarocco

		marocco = PyMarocco()
		pynn.setup(marocco = marocco)

Make sure that the call to ``pynn.setup`` happens before creating
populations, if not, the populations will not be visible to ``marocco``.

Now it is time to start marocco. When invoking ``python``, an MPI
library has to be preloaded.

.. code-block:: bash

	LD_PRELOAD=/usr/lib/openmpi/lib/libmpi.so python main.py

If you don't preload libmpi, the error message is:

.. code-block:: bash

	python: symbol lookup error: /usr/lib/openmpi/lib/openmpi/mca_paffinity_linux.so:
		undefined symbol: mca_base_param_reg_int

If pyNN.recording.files cannot be imported, pyNN is missing from your paths:

.. code-block:: python

	Traceback (most recent call last):
	  File "main.py", line 5, in <module>
		import pyhmf as pynn
	ImportError: No module named pyNN.recording.files

You can add pyNN to your paths by loading the module:

.. code-block:: bash

	module load pynn/0.7.5

In the following example, one neuron is placed on the wafer, however,
by choosing the backend None, the actual hardware is not used.

Available backends: None, Hardware, ESS. None does only mapping and
routing (a dry run). Hardware runs on the real neuromorphic
hardware. ESS runs a simulation of the hardware: the Executable System
Specification.

.. code-block:: python

		import pyhmf as pynn
		from pymarocco import PyMarocco

		marocco = PyMarocco()
		marocco.backend = PyMarocco.None

		pynn.setup(marocco = marocco)

		neuron = pynn.Population(1, pynn.IF_cond_exp)

		pynn.run(10)
		pynn.end()

In the output you should see:

.. code-block:: bash


		Populations:
                0th element:    0x1f98650       Population(IF_cond_exp, 1)


If you don't see this output, make sure that you called
``pynn.setup(marocco = marocco)`` before the call to
``pynn.Population``.

You will also see a lot of debug output. To set the log level, add

.. code-block:: python

   import pylogging
   for domain in [""]:
	pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.ERROR)

after the line importing ``PyMarocco`` to your script.

As we did not specify on which chip the neuron should be placed,
marocco decides automatically to use ``HICANNOnWafer(X(18), Y(7)),
Wafer(0)`` which is in the center of the wafer.

To choose the HICANN a population is placed on, we give marocco a hint:

.. code-block:: python

		import Coordinate as C

		marocco.manual_placement.on_hicann(neuron, C.HICANNOnWafer(C.X(5), C.Y(5)))

At the end, the script is the following:

nmpm1_marocco_intro.py:

.. literalinclude:: examples/nmpm1_marocco_intro.py

We also added a print out of the chosen neuron circuits:

.. code-block:: bash

		NeuronOnWafer(NeuronOnHICANN(X(0), top), HICANNOnWafer(X(5), Y(5)))
		NeuronOnWafer(NeuronOnHICANN(X(1), top), HICANNOnWafer(X(5), Y(5)))
		NeuronOnWafer(NeuronOnHICANN(X(0), bottom), HICANNOnWafer(X(5), Y(5)))
		NeuronOnWafer(NeuronOnHICANN(X(1), bottom), HICANNOnWafer(X(5), Y(5)))

Calibration
'''''''''''

To change the calibration backend from database to XML set
"calib_backend" to XML. Then the calibration is looked up in xml files
named ``w0-h84.xml``, ``w0-h276.xml``, etc. in the directory
"calib_path".

.. _label-marocco-example:

Running pyNN scripts
''''''''''''''''''''

To run on the *hardware* one needs to use the slurm job queue system:

.. code-block:: bash

	srun -p wafer python nmpm1_single_neuron.py

nmpm1_single_neuron.py:

.. literalinclude:: examples/nmpm1_single_neuron.py

Inspect the Configuration
'''''''''''''''''''''''''

.. code-block:: bash

    sthal/tools/dump_cfg.py

Inspect the synapse loss
------------------------

When mapping network models to the wafer-scale hardware, it may happen that not
all model synapses can be realized on the hardware due to limited hardware
resources. Below is a simple network that is mapped to very limited resources
so that synapse loss is enforced. For this example we show how to extract
overall mapping statistics and projection-wise or synapse-wise synapse losses.

.. literalinclude:: examples/synapse_loss.py
   :pyobject: main


Where ``print marocco.stats`` prints out overall synapse loss statistics:

.. code-block:: bash

    MappingStats {
            synapse_loss: 581 (23.3709%)
            synapses: 2486
            synapses set: 1905
            synapses lost: 581
            synapses lost(l1): 0
            populations: 2
            projections: 2
            neurons: 50}

Invidual mapping statistics like the number of synapses set can also be
directly accessed in python, see class ``MappingStats`` in
`documentation-marocco`_.

The function ``projectionwise_synapse_loss`` shows how to calculate the synapse
loss per projection.

.. literalinclude:: examples/synapse_loss.py
   :pyobject: projectionwise_synapse_loss

Which yields the following oubput for the example above:

.. code-block:: bash

    Projection-Wise Synapse Loss Projection ( PyAssembly (50) -> PyAssembly (50)) 23.5576923077
    Projection-Wise Synapse Loss Projection ( PyAssembly (50) -> PyAssembly (50)) 23.182552504


Finally, the function ``plot_projectionwise_synapse_loss`` can be used to plot
the lost and realized synapses of one projection.

.. literalinclude:: examples/synapse_loss.py
   :pyobject: plot_projectionwise_synapse_loss

.. figure:: examples/synapse_loss.png
   :alt: Realized and Lost Synapses of a Projection

   Realized (black) and lost (red) synapses of the stimulus projection in the
   example network above.
