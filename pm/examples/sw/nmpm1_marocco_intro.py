#!/usr/bin/env python

import pyhmf as pynn
import Coordinate as C
from pymarocco import PyMarocco, Defects
from pymarocco.results import Marocco

import pylogging
for domain in ["Calibtic", "marocco"]:
    pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.INFO)

marocco = PyMarocco()
marocco.calib_backend = PyMarocco.CalibBackend.Default
marocco.defects.backend = Defects.Backend.None
marocco.neuron_placement.skip_hicanns_without_neuron_blacklisting(False)
marocco.persist = "results.bin"
pynn.setup(marocco = marocco)

pop = pynn.Population(1, pynn.IF_cond_exp)

marocco.manual_placement.on_hicann(pop, C.HICANNOnWafer(C.X(5), C.Y(5)), 4)

pynn.run(10)
pynn.end()

results = Marocco.from_file(marocco.persist)

for neuron in pop:
    for item in results.placement.find(neuron):
        for denmem in item.logical_neuron():
            print denmem
