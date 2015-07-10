Testing the system
==================

.. warning:: this section is work in progress

To run all tests taking in total several minutes first setup environment (:ref:`label-beforeexp`), then:

.. code-block:: bash

    cd symap2ic/test
    sh run_spikey_tests.sh

For low-level tests taking only several seconds use:

.. code-block:: bash

    cd symap2ic/bin/test
    ./test-main --gtest_filter=-*Inf
