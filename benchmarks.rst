==========
Benchmarks
==========

Benchmarking of neuromorphic hardware puts numbers on performance to allow measuring progress and comparing different
designs.
This is useful both for the developers of the Neuromorphic Computing Platform and for potential users.

Specifically, benchmarks define a set of reference tasks aiming at a direct comparison of different neuromorphic
(and non-neuromorphic) hardware systems.
Each benchmark has a set of quality measures.
It is left to the user to decide which specific measures are relevant for the particular application in mind.


Developing benchmarks
=====================

Defining models and tasks
-------------------------

As stated above, all benchmark code should be under version control.
Each repository may contain one or more models, and for each model one or more tasks should be defined.
The top-level of the repository should contain a JSON-format configuration file named "benchmarks.json", with
the following general structure:

.. code-block:: json

    [
      {
        "model": {
          "name": "ModelA",
          "description": "Description of model A"
        },
        "tasks": [
          {
            "name": "taskA1",
            "command": "task_1_for_model_A.py {system}"
          },
          {
            "name": "taskA2",
            "command": "task_2_for_model_A.py arg1 {system}"}
          }
        ]
      },
      {
        "model": {
          "name": "ModelB",
          "description": "Description of model B"
        },
        "tasks": [
          {
            "name": "taskB1",
            "command": "task_1_for_model_B.py {system}"
          },
          {
            "name": "taskB2",
            "command": "task_2_for_model_B.py arg1 {system}"
          },
          {
            "name": "taskB3alpha",
            "command": "task_3_for_model_B.py --option1={system} arg1 arg2 arg3"
          },
          {
            "name": "taskB3beta",
            "command": "task_3_for_model_B.py --option1={system} arg4 arg5 arg6"
          },
        ]
      }
    ]


i.e., each task should be expressed as a command-line invocation of a Python script. The Python script should
 in general use the PyNN API, in which case the placeholder "{system}" must be provided, and will be replaced by
 the name of the PyNN backend used when running the benchmark, e.g. "nest", "spiNNaker", or "hardware.hbp_pm".
 If the benchmark is known to run only on a subset of the available backends, this can be indicated by listing
 the suitable backends within the placeholder, e.g. "{system=spiNNaker,nest}".
 For low-level benchmarks for a single neuromorphic system, the Python script should use the low-level APIs of that platform,
 and in this case the "{system}" placeholder should be absent.


A specific example, for the repository https://github.com/CNRS-UNIC/hardware-benchmarks, is:

.. code-block:: json

    [
      {
        "model": {
          "name": "IF_cond_exp",
          "description": "A population of IF neurons, each of which is injected with a different current"
        },
        "tasks": [
          {
            "name": "I_f_curve",
            "command": "run_I_f_curve.py {system}"
          }
        ]
      },
      {
        "model": {
          "name": "SpikeSourcePoisson",
          "description": "A population of random spike sources, each with different firing rates"
        },
        "tasks": [
          {
            "name": "run20s",
            "command": "run_spike_train_statistics.py {system}"
          }
        ]
      }
    ]


Returning numerical measures
----------------------------


Each task should run a simulation of a neuronal network model, record data from the neurons,
perform analysis of the data, and calculate numerical measures of the system performance.
The numerical measures should be reported in a JSON-format file, consisting of a top-level
record with required fields "timestamp" and "results". The field "configuration", containing
a copy of the parameterization of the model and simulator/hardware system", is optional.
The field "results" contains a list of records with the following fields:

**type**
    What is being measured. For example "quality", "performance", "energy consumption".
**name**
   A unique name for the measurement. It is suggested that this name takes the form of a URI
   containing the URL of the version control repository followed by an identifier for the task
   and an identifier for the measurement.
**value**
    A floating point number.
**units**
    (optional) if the measurement is a physical quantity, the units of the quantity using SI nomenclature.
**measure**
    the type of the measurement, for example "norm", "p-value", "time".

(A controlled vocabulary will be developed for the fields "type" and "measure").

Here is an example:

.. code-block:: json

    ﻿{
        "timestamp": "2015-06-05T11:13:59.535885",
        "results": [
            {
                "type": "quality",
                "name": "norm_diff_frequency",
                "value": 0.0073371188622418891,
                "measure": "norm"
            },
            {
                "type": "performance",
                "name": "setup_time",
                "value": 0.026206016540527344,
                "units": "s",
                "measure": "time"
            },
            {
                "type": "performance",
                "name": "run_time",
                "value": 1.419724941253662,
                "units": "s",
                "measure": "time"
            },
            {
                "type": "performance",
                "name": "closing_time",
                "value": 0.03272294998168945,
                "units": "s",
                "measure": "time"
            }
        ],
    }


The task may also optionally produce figures and other output data files.

Registering benchmarks
----------------------

To add a new benchmark model or task within an existing repository, just modify the "benchmarks.json" configuration file.
To add a new repository, e-mail andrew.davison@unic.cnrs-gif.fr.
In future, a web form for registering new repositories will be introduced.


Running benchmarks
------------------

A continuous integration system will be put in place, which will run the entire suite of benchmarks
on each neuromorphic system every time the system configuration (software or hardware) is changed,
and which will run the benchmarks from a given repository on both neuromorphic systems (where appropriate)
each time a new commit is made to the repository. To indicate that a given commit should *not* trigger
a run (for example because only documentation has been changed),
include the text "[skip ci]" or "[ci skip]" within the commit message.

After running each task, the continous integration system will harvest the JSON-formatted measurement report,
and update a database of benchmark measurements. This benchmark database will be visualized in an "App"
within the HBP Neuromorphic Platform Collaboratory.