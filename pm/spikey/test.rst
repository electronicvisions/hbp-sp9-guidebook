Testing the system
==================

.. warning:: this section is work in progress

First, setup the environment variables.
Then, to run all tests use:

.. code-block:: bash

    cd spikey_demo/test
    sh run_spikey_tests.sh

In total this will take several minutes.

For low-level tests that take only several seconds, use:

.. code-block:: bash

    cd spikey_demo/bin/tests
    ./test-main --gtest_filter=-*Inf
