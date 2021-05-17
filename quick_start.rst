.. _quick_start:

===============
Getting started
===============

To use the Neuromorphic Computing systems you will need to:

1. create an EBRAINS account (`available on request`_), free of charge
2. send an email with your EBRAINS username to neuromorphic@humanbrainproject.eu

You will then get a Collab created with a test-quota to access the BrainScaleS and SpiNNaker machines, 
pre-loaded with some examples how to access the systems. (The "Collab" is a collaborative workspace)

You can then:

* Add team members to your Collab using the ":guilabel:`Team`" link in the navigation bar on the left.
  Only members of the team will be able to launch simulations.
* Run simulations, using the ":guilabel:`Job Manager`" link or via the Jupyter notebooks available in the ":guilable:`Lab`"


Run a simulation
================

Simulations can be run via Jupyter notebooks (use the ":guilabel:`Lab`") or 
can be submitted via the ":guilabel:`Job Manager`". 

Running via JupyterLab via NMPI ("batch" operation)
------------------------------
To submit a simulation in "batch" mode using the Jupyter notebooks via the ":guilabel:`Lab`":

#. open one of the example notebooks 
#. execute the cells. This:

   #. prepares the execution environment
   #. writes the experiment description PyNN script as a file 
   #. sends this file (in the ```job = client.submit_job( ...)``` step) to the SpiNNaker system in Manchester or 
      the BrainScaleS system in Heidelberg
   #. waits for the job to finish
   #. transfers the result files back to the system, where the Jupyter process is running on the Collab

The results can then be shown and analysed in the notebook.

As this mode of operation sends the experiment description as file to the machine site for execution and then waits
for the result files to be transferred back, there is no interactive interaction with the running network
simulation (SpiNNaker) or emulation (BrainScaleS) network possible ("batch" operation).


Running via the JobManager ("batch" operation)
--------------------------

To submit a simulation via the ":guilabel:`Job Manager`": 

#. oben the ":guilabel:`Job Manager`" from the left hand navigation of your Collab
#. press ":guilabel:`+`" icon in the table header to add a new job
#. in the "New job" form 

   #. select "SpiNNaker" in the :guilabel:`Hardware Platform` drop-down menu
   #. then enter Python code in the ":guilabel:`Code`" text box, for example the following short script, which simulates a population of integrate-and-firing neurons with different input firing rates:

.. code-block:: python

   """
   A population of integrate-and-firing neurons with different input firing rates
   """

   import numpy as np
   import matplotlib.pyplot as plt
   import pyNN.spiNNaker as sim

   sim.setup(timestep=1.0, min_delay=1.0)

   # create cells
   cell_params = {
       'cm': 0.25, 'tau_m': 10.0, 'tau_refrac': 2.0,
       'tau_syn_E': 2.5, 'tau_syn_I': 2.5,
       'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -55.0}

   neurons = sim.Population(100, sim.IF_cond_exp(**cell_params))
   inputs = sim.Population(100, sim.SpikeSourcePoisson(rate=0.0))

   # set input firing rates as a linear function of cell index
   input_firing_rates = np.linspace(0.0, 1000.0, num=inputs.size)
   inputs.set(rate=input_firing_rates)

   # create one-to-one connections
   wiring =  sim.OneToOneConnector()
   static_synapse = sim.StaticSynapse(weight=0.1, delay=2.0)
   connections = sim.Projection(inputs, neurons, wiring, static_synapse)

   # configure recording
   neurons.record('spikes')

   # run simulation
   sim_duration = 10.0 # seconds
   sim.run(sim_duration * 1000.0)

   # retrieve recorded data
   spike_counts = neurons.get_spike_counts()
   print(spike_counts)
   output_firing_rates = np.array(
       [value for (key, value) in sorted(spike_counts.items())])/sim_duration

   # plot graph
   plt.plot(input_firing_rates, output_firing_rates)
   plt.xlabel("Input firing rate (spikes/second)")
   plt.ylabel("Output firing rate (spikes/second)")
   plt.savefig("simple_example.png")

..

   3. Leave the other text boxes empty, and click ":guilabel:`Submit`".

The job will be submitted to the queue, and will appear in the list of jobs with a "submitted" label.
Unless the platform is very busy, this job should run within a few minutes on the large-scale
SpiNNaker system in Manchester.
Once the simulation is finished you will receive an e-mail, and on refreshing the job list the
status will change to "finished".

.. image:: images/ebrains_job_manager.png
   :width: 70%
   :align: center

Once the job is completed, click on the magnifying glass icon to see the job results.

.. image:: images/ebrains_job_manager_jobresult.png
   :width: 70%
   :align: center

In the "Output files" part you will find a link to the created plot (a .png file):

.. image:: images/ebrains_job_manager_jobresult_figure.png
   :width: 70%
   :align: center


For more information on running simulations with the platform, see :ref:`running-jobs`.

Copy data to longer-term storage
================================

The results of your simulation are now available on a file server attached to the
SpiNNaker system. This storage is only temporary, however; after three months, your files may
be deleted to free up space.

If you need to keep the files please download them to your local machine.

.. For now we will copy the files to Collab Storage by clicking the button ":guilabel:`Copy to Collab storage`".
.. If you now click on the link ":guilabel:`Storage`" in the left-hand menu, you will see the files produced by your simulation.
.. add screenshot of Storage

.. add a note about the limitations of Collab storage.


When the test-quota is used up
=================================

Using the :guilabel:`Job Manager` you can request more quota (only needed, when the test quota 
has been used up). 



.. _`available on request`: https://ebrains.eu/register
.. _Collaboratory: https://wiki.ebrains.eu/bin/view/Collabs/neuromorphic/
