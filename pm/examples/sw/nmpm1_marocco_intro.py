#!/usr/bin/env python

import pyhmf as pynn
from pyhalco_common import Enum, X, Y
from pyhalco_hicann_v2 import HICANNOnWafer
from pymarocco import PyMarocco, Defects
from pymarocco.results import Marocco

import pylogging
for domain in ["Calibtic", "marocco"]:
    pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.INFO)

def get_denmems(pop, results):
    for neuron in pop:
        for item in results.placement.find(neuron):
            for denmem in item.logical_neuron():
                yield denmem

marocco = PyMarocco()
marocco.calib_backend = PyMarocco.CalibBackend.Default
marocco.defects.backend = Defects.Backend.None
marocco.neuron_placement.skip_hicanns_without_neuron_blacklisting(False)
marocco.persist = "results.xml.gz"
pynn.setup(marocco = marocco)

# place the full population to a specific HICANN
pop = pynn.Population(1, pynn.IF_cond_exp)
marocco.manual_placement.on_hicann(pop, HICANNOnWafer(X(5), Y(5)), 4)

# place only parts of a population
pop2 = pynn.Population(3, pynn.IF_cond_exp)
marocco.manual_placement.on_hicann(pynn.PopulationView(pop2, [0]), HICANNOnWafer(Enum(5)))
marocco.manual_placement.on_hicann(pynn.PopulationView(pop2, [1]), HICANNOnWafer(Enum(1)))
# the third neuron will be automatically placed

pynn.run(10)
pynn.end()

results = Marocco.from_file(marocco.persist)

for denmem in get_denmems(pop, results):
    print denmem

for denmem in get_denmems(pop2, results):
    print denmem
