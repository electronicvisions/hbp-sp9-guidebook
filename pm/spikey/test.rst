Testing the system
==================

.. warning:: this section is work in progress

First, setup the environment (see :ref:`label-softwaremodule`).
Then, to run all tests use:

.. code-block:: bash

    cd symap2ic/test
    sh run_spikey_tests.sh

In total this will take several minutes.

For low-level tests that take only several seconds, use:

.. code-block:: bash

    cd symap2ic/bin/test
    ./test-main --gtest_filter=-*Inf
